# get_stream_dev
Note: you have to pass a URI when executing the binary.

- cf-ad9361-dds-core-lpc: fpga-low pin count signal generator (dds)
- cf-ad9361-lpc: fpga low pin count

# Finding devices to access
Inside
```bash
cd /sys/bus/iio/devices

# Command that reveals all the devices and its attributes
iio_info –u ip:192.168.2.1
```
You can find the 
- iio:device0 (ad9361-phy) - Device Global Settings
    - LO 
    - voltages
    - (everything to do with the ad9361-chip, oscillators, voltages, temperatures, offsets, ..)
- iio:device1 (xadc) - Receive Chain
- iio:device2 (cf-ad9361-dds-core-lpc) - Tx device
- iio:device3 (cf-ad9361-lpc) - RX device

## RX / TX, Ports / channels
RX and TX ports 0 is the ones we use. (these are the ones connected).
- in_voltage0: RX1 - default RX channel enabled
- in_voltage_1
- out_voltage0: TX1 -default TX channel enabled
- out_voltage_1: TX

## Local oscillators
- out_altvoltage1_TX_LO_frequency: TX local oscillator
- out_altvoltage0_RX_LO_frequency: RX local oscillator

In case we want to modify parameters, we can always do as follows:
```bash
echo 2450000000 >  out_altvoltage0_RX_LO_frequency
cat out_altvoltage0_RX_LO_frequency
# RX local oscillator frequency should now be at 2.45 GHz Hz
```

## Reading from device
```bash
# List contexts provided, choose one of those listed
iio_readdev -S
# e.g.:
iio_readdev -u usb:3.11.5 -b 4096 -s 65536 cf-ad9361-lpc | pv > raw_data.dat
iio_readdev -u ip:pluto.local -b 4096 -s 65536 cf-ad9361-lpc | pv > raw_data.dat
# Opens device context after "-u", reads a total of 65536 samples with buffer sizes of 4096.
```

### raw_data.dat
The file looks as follows:
- I0 (int16), Q0 (int16), I1 (int16), Q1 (int16), ..., I(n) (int16), Q(n) (int16)

Print using
```bash
xxd raw_data.dat | head
```


## Resource
-  Full guide on possible iio settings for ad9361: https://wiki.analog.com/resources/tools-software/linux-drivers/iio-transceiver/ad9361
- AD936x: https://wiki.analog.com/resources/tools-software/linux-software/fmcomms2_advanced_plugin
- Device tree drivers for linux AD9361: https://wiki.analog.com/resources/tools-software/linux-drivers/iio-transceiver/ad9361-customization
- Full guide

# libiio
- example of plotting with gnuplot https://ez.analog.com/adieducation/university-program/f/q-a/581166/gnuplot-yields-double-buffer-size-when-plotting-using-libiio

# Math libraries
We need to find math libraries which preferably can be
- Cross-compiled on the pluto-sdr
- Are available for ubuntu
- Have a wide variety of DSP functionality
    - DFT (discrete fourier transform)
    - Demodulation
    - Filtering
- Have regular math functionality
    - Min
    - Max
    - Std

# Plotting libraries
We need plotting libraries which give the possibility to be
- Cross-compiled on the pluto-sdr (optional, in case we'd like to skip this part and simply import the data onto the server after processing instead)
- Are available for ubuntu

Perhaps go with matplotlib, and use a script to simply plot the saved data.
