// SPDX-License-Identifier: GPL-2.0-or-later
/*
 * libiio - AD9361 IIO streaming example
 *
 * Copyright (C) 2014 IABG mbH
 * Author: Michael Feilen <feilen_at_iabg.de>
 **/

#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <signal.h>
#include <stdio.h>
#include <iio.h>
#include <math.h>

#include <errno.h>
#include "csv_writer.h"

/* helper macros */
#define MHZ(x) ((long long)(x*1000000.0 + .5))
#define GHZ(x) ((long long)(x*1000000000.0 + .5))

#define F_MOD	12e3

/**
 * Triggered if false is returned
 */
#define IIO_ENSURE(expr) { \
	if (!(expr)) { \
		(void) fprintf(stderr, "assertion failed (%s:%d)\n", __FILE__, __LINE__); \
		(void) abort(); \
	} \
}

/* RX is input, TX is output */
enum iodev { RX, TX };

/* common RX and TX streaming params */
struct stream_cfg {
	long long bw_hz; // Analog banwidth in Hz
	long long fs_hz; // Baseband sample rate in Hz
	long long lo_hz; // Local oscillator frequency in Hz
	const char* gain_ctrl_mode;
	double hw_gain;
	const char* rfport; // Port name
};

/* static scratch mem for strings */
static char tmpstr[64];

/* IIO structs required for streaming */
static struct iio_context *ctx   = NULL;
static struct iio_channel *rx0_i = NULL;
static struct iio_channel *rx0_q = NULL;
static struct iio_channel *tx0_i = NULL;
static struct iio_channel *tx0_q = NULL;
static struct iio_buffer  *rxbuf = NULL;
static struct iio_buffer  *txbuf = NULL;

static bool stop;

/* cleanup and exit */
static void shutdown(void)
{
	printf("* Destroying buffers\n");
	if (rxbuf) { iio_buffer_destroy(rxbuf); }
	if (txbuf) { iio_buffer_destroy(txbuf); }

	printf("* Disabling streaming channels\n");
	if (rx0_i) { iio_channel_disable(rx0_i); }
	if (rx0_q) { iio_channel_disable(rx0_q); }
	if (tx0_i) { iio_channel_disable(tx0_i); }
	if (tx0_q) { iio_channel_disable(tx0_q); }

	printf("* Destroying context\n");
	if (ctx) { iio_context_destroy(ctx); }
	exit(0);
}

static void handle_sig(int sig)
{
	printf("Waiting for process to finish... Got signal %d\n", sig);
	stop = true;
}

/* check return value of attr_write function */
static void errchk(int v, const char* what) {
	 if (v < 0) { fprintf(stderr, "Error %d writing to channel \"%s\"\nvalue may not be supported.\n", v, what); shutdown(); }
}

/* write attribute: long long int */
static void wr_ch_lli(struct iio_channel *chn, const char* what, long long val)
{
	errchk(iio_channel_attr_write_longlong(chn, what, val), what);
}

/* write attribute: string */
static void wr_ch_str(struct iio_channel *chn, const char* what, const char* str)
{
	errchk(iio_channel_attr_write(chn, what, str), what);
}

/* write attribute: double */
static void wr_ch_d(struct iio_channel *chn, const char* what, double val)
{
	errchk(iio_channel_attr_write_double(chn, what, val), what);
}


/* helper function generating channel names */
static char* get_ch_name(const char* type, int id)
{
	snprintf(tmpstr, sizeof(tmpstr), "%s%d", type, id);
	return tmpstr;
}

/* returns ad9361 phy device */
static struct iio_device* get_ad9361_phy(void)
{
	struct iio_device *dev =  iio_context_find_device(ctx, "ad9361-phy");
	IIO_ENSURE(dev && "No ad9361-phy found");
	return dev;
}

/* finds AD9361 streaming IIO devices */
static bool get_ad9361_stream_dev(enum iodev d, struct iio_device **dev)
{
	switch (d) {
	case TX: 
		*dev = iio_context_find_device(ctx, "cf-ad9361-dds-core-lpc");
		printf("TX_dev: %p val: %p\r\n", dev, *dev); 
		return *dev != NULL;
	case RX: 
		*dev = iio_context_find_device(ctx, "cf-ad9361-lpc");  
		printf("RX_dev: %p\r\n", dev); 
		return *dev != NULL;
	default: IIO_ENSURE(0); return false;
	}
}

/* finds AD9361 streaming IIO channels */
static bool get_ad9361_stream_ch(enum iodev d, struct iio_device *dev, int chid, struct iio_channel **chn)
{
	*chn = iio_device_find_channel(dev, get_ch_name("voltage", chid), d == TX);
	if (!*chn)
	{
		// Get the local oscillator channel name and see if it's found.
		*chn = iio_device_find_channel(dev, get_ch_name("altvoltage", chid), d == TX);
	}
	return *chn != NULL;
}

/* finds AD9361 phy IIO configuration channel with id chid */
static bool get_phy_chan(enum iodev d, int chid, struct iio_channel **chn)
{
	switch (d) {
	case RX: *chn = iio_device_find_channel(get_ad9361_phy(), get_ch_name("voltage", chid), false); return *chn != NULL;
	case TX: *chn = iio_device_find_channel(get_ad9361_phy(), get_ch_name("voltage", chid), true);  return *chn != NULL;
	default: IIO_ENSURE(0); return false;
	}
}

/* finds AD9361 local oscillator IIO configuration channels */
static bool get_lo_chan(enum iodev d, struct iio_channel **chn)
{
	switch (d) {
	 // LO chan is always output, i.e. true
	case RX: *chn = iio_device_find_channel(get_ad9361_phy(), get_ch_name("altvoltage", 0), true); return *chn != NULL;
	case TX: *chn = iio_device_find_channel(get_ad9361_phy(), get_ch_name("altvoltage", 1), true); return *chn != NULL;
	default: IIO_ENSURE(0); return false;
	}
}

/* applies streaming configuration through IIO */
bool cfg_ad9361_streaming_ch(struct stream_cfg *cfg, enum iodev type, int chid)
{
	struct iio_channel *chn = NULL;

	// Configure phy and lo channels
	printf("Go\r\n");
	printf("* Acquiring AD9361 phy channel %d\n", chid);
	if (!get_phy_chan(type, chid, &chn)) {	return false; }
	wr_ch_str(chn, "rf_port_select",     cfg->rfport);
	wr_ch_lli(chn, "rf_bandwidth",       cfg->bw_hz);
	wr_ch_lli(chn, "sampling_frequency", cfg->fs_hz);

	// Configure LO channel
	if (type == RX)
	{
		wr_ch_str(chn, "gain_control_mode", cfg->gain_ctrl_mode);
	}
	if (cfg->gain_ctrl_mode == "manual")
	{
		wr_ch_d(chn, "hardwaregain", cfg->hw_gain);
	}

	printf("* Acquiring AD9361 %s lo channel\n", type == TX ? "TX" : "RX");
	if (!get_lo_chan(type, &chn)) { return false; }
	wr_ch_lli(chn, "frequency", cfg->lo_hz);
	return true;
}

/* simple configuration and streaming */
/* usage:
 * Default context, assuming local IIO devices, i.e., this script is run on ADALM-Pluto for example
 $./a.out
 * URI context, find out the uri by typing `iio_info -s` at the command line of the host PC
 $./a.out usb:x.x.x
 * e.g: [/ads9361_test ip:192.168.2.1]
 */
int main (int argc, char **argv)
{

	// Streaming devices
	struct iio_device *tx;
	struct iio_device *rx;

	// RX and TX sample counters
	size_t nrx = 0;
	size_t ntx = 0;

	// Stream configurations
	struct stream_cfg rxcfg;
	struct stream_cfg txcfg;


	bool cyclical = false;
	// Listen to ctrl+c and IIO_ENSURE
	signal(SIGINT, handle_sig);

	// RX stream config
	rxcfg.bw_hz = MHZ(2);   // 2 MHz rf bandwidth
	rxcfg.fs_hz = MHZ(2.5); // 2.5 MS/s rx sample rate
	rxcfg.lo_hz = GHZ(2.5); // 2.5 GHz rf frequency
	rxcfg.rfport = "A_BALANCED"; // port A (select for rf freq.)

	// TX stream config
	txcfg.bw_hz = MHZ(1.5); // 1.5 MHz rf bandwidth
	txcfg.fs_hz = MHZ(2.5);   // 2.5 MS/s tx sample rate
	txcfg.lo_hz = GHZ(2.5); // 2.5 GHz rf frequency
	txcfg.rfport = "A"; // port A (select for rf freq.)

	printf("* Acquiring IIO context\n");
	if (argc == 1) {
		IIO_ENSURE((ctx = iio_create_default_context()) && "No context");
	}
	else if (argc == 2) {
		IIO_ENSURE((ctx = iio_create_context_from_uri(argv[1])) && "No context");
	}
	IIO_ENSURE(iio_context_get_devices_count(ctx) > 0 && "No devices");

	printf("* Acquiring AD9361 streaming devices\n");
	IIO_ENSURE(get_ad9361_stream_dev(TX, &tx) && "No tx dev found");
	IIO_ENSURE(get_ad9361_stream_dev(RX, &rx) && "No rx dev found");

	printf("* Configuring AD9361 for streaming_\n");
	rxcfg.hw_gain = 0;
	rxcfg.gain_ctrl_mode = "manual";
	IIO_ENSURE(cfg_ad9361_streaming_ch(&rxcfg, RX, 0) && "RX port 0 not found");
	
	txcfg.hw_gain = -20;
	IIO_ENSURE(cfg_ad9361_streaming_ch(&txcfg, TX, 0) && "TX port 0 not found");

	printf("* Initializing AD9361 IIO streaming channels\n");
	IIO_ENSURE(get_ad9361_stream_ch(RX, rx, 0, &rx0_i) && "RX chan i not found");
	IIO_ENSURE(get_ad9361_stream_ch(RX, rx, 1, &rx0_q) && "RX chan q not found");
	IIO_ENSURE(get_ad9361_stream_ch(TX, tx, 0, &tx0_i) && "TX chan i not found");
	IIO_ENSURE(get_ad9361_stream_ch(TX, tx, 1, &tx0_q) && "TX chan q not found");

	printf("* Enabling IIO streaming channels\n");
	iio_channel_enable(rx0_i);
	iio_channel_enable(rx0_q);
	iio_channel_enable(tx0_i);
	iio_channel_enable(tx0_q);

	printf("* Creating non-cyclic IIO buffers with 1 MiS\n");
	size_t bitsize = 1024*32;
	rxbuf = iio_device_create_buffer(rx, bitsize, false);
	int ret = iio_buffer_set_blocking_mode(rxbuf, false);
	if (!rxbuf) {
		perror("Could not create RX buffer");
		shutdown();
	}
	if (ret) {
		printf("err: %d", ret);
		perror("Setting RX buffer to blocking failed\r\n");
		shutdown();
	}
	txbuf = iio_device_create_buffer(tx, bitsize, cyclical);
	ret = iio_buffer_set_blocking_mode(txbuf, false);
	if (!txbuf) {
		perror("Could not create TX buffer");
		shutdown();
	}
	if (ret) {
		printf("err: %d", ret);
		perror("Setting TX buffer to blocking failed\r\n");
		shutdown();
	}
	size_t n_samples = (bitsize / 16) * 2;
	
	
	int idx = 0;
	
	int tx_busy;
	int rx_busy;
	printf("* Starting IO streaming (press CTRL+C to cancel)\n");
	while ((!stop) && (idx < 100))
	{
		//! READ BYTES

		int n_samples_rx = 0;
		int n_samples_tx = 0;

		ssize_t nbytes_rx, nbytes_tx;
		char *p_dat, *p_end;
		ptrdiff_t p_inc, t_inc;

		// Schedule TX buffer
		uint32_t *buffer_tx = iio_buffer_first(txbuf, rx0_i);
		if (!(cyclical && (idx != 0)))
		{
			for (int i=0; i<n_samples; i++)
			{
				//! t -> index should take timesteps equal to the sampling periodc
				//!   -> frequency of the sine should be F_MOD
				double t_index = ((double) i) / (double) txcfg.fs_hz;
				// printf("t_index: %.6f", t_index);
				int16_t ipart = (int16_t)(pow(2, 15)) * sin(2.0 * (double)M_PI * (t_index * (double)(F_MOD)));
				int16_t qpart = (int16_t)(pow(2, 15)) * cos(2.0 * (double)M_PI * (t_index * (double)(F_MOD)));
				buffer_tx[i] = (ipart << 16) | (qpart & 0xFFFF);
			}
			while (iio_buffer_push(txbuf) == -EAGAIN){;}
		}
		if (nbytes_tx < 0) { printf("Error pushing buf %d\n", (int) nbytes_tx); shutdown(); }
		n_samples_tx = nbytes_tx / iio_device_get_sample_size(tx);

		// Refill RX buffer
		while (iio_buffer_refill(rxbuf)) {;}
		// nbytes_rx = iio_buffer_refill(rxbuf) ;

		n_samples_rx = nbytes_rx / iio_device_get_sample_size(rx);


		if (nbytes_rx < 0) { printf("Error refilling buf %d\n",(int) nbytes_rx); shutdown(); }

		// READ: Get pointers to RX buf and read IQ from RX buf port 0
		p_inc = (ptrdiff_t)iio_buffer_step(rxbuf);		
		p_end = (char*)iio_buffer_end(rxbuf);

		printf("samplesize p_inc: %ld\r\n", p_inc);
		printf("rx bufstart: %p\r\n", iio_buffer_first(rxbuf, rx0_i));
		
		t_inc = (ptrdiff_t)iio_buffer_step(txbuf);
		printf("samplesize t_inc: %ld\r\n\r\n", t_inc);
		printf("tx bufstart: %p\r\n", iio_buffer_first(txbuf, tx0_i));
		
		char filename_rx[30];
		char filename_tx[30];

		sprintf(filename_rx, "sam_rx_%d", idx);
		sprintf(filename_tx, "sam_tx_%d", idx);

		uint32_t *buffer_rx = iio_buffer_first(rxbuf, rx0_i);

		save_as_csv((uint32_t*)iio_buffer_first(rxbuf, rx0_i), nbytes_rx, filename_rx);
		if (!(cyclical && (idx != 0)))
		{
			save_as_csv((uint32_t*)iio_buffer_first(txbuf, tx0_i), nbytes_tx, filename_tx);
		}

		// Sample counter increment and status output
		nrx += nbytes_rx / iio_device_get_sample_size(rx);
		ntx += nbytes_tx / iio_device_get_sample_size(tx);
		printf("\tRX %8.2f MSmp, TX %8.2f MSmp\n", nrx/1e6, ntx/1e6);
		idx++;
	}

	shutdown();

	return 0;
}
