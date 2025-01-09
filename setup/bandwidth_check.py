
import numpy as np
import adi, math
import matplotlib.pyplot as plt
import time

sample_rate = 10e6 # Hz
num_samps = 1024*512 # number of samples per call to rx()
center_freq = 915e6 # Hz

sdr = adi.Pluto("ip:192.168.2.1")
# sdr = adi.Pluto("usb:3.5.5")
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 0.0 # dB, increase to increase the receive gain, but be careful not to saturate the ADC
sdr.rx_lo = int(center_freq)

sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = int(num_samps)

n_meas = 10
while (1):
    print(f"sample_rate: {sample_rate} - n_samples_tot {num_samps}")
    time_tot = 0
    for i in range(n_meas):
        time_start = time.time()
        sdr.rx()
        time_tot += time.time() - time_start

    # If the time is greater than the expected time it would take
    # OR the amount of samples is not adequate
    # BREAK
    print(f"time_tot: {time_tot} n_samples: {n_meas*num_samps} sample_rate: {n_meas * num_samps / time_tot}")
    print(f"time_tot_exp: {(n_meas * num_samps) / sample_rate}, n_samples_expected: {n_meas*num_samps}")

    # num_samps -= 5
    sample_rate -= 1e5
    sdr.sample_rate = int(sample_rate)
    sdr.rx_rf_bandwidth = int(sample_rate)

    print(f"-----------------------------------------")

'''
The reason why the USB-throughput is optimal at buffer sizes higher than 1024 * 128 is likely because the internal buffers of the iio-libs
have this size by default.
'''