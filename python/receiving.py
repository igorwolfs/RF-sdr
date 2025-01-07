#! TEST: https://pysdr.org/content/pluto.html


import numpy as np
import adi
import time
# Set the sample rate to 1 MHz
sample_rate = 2000e6 # Hz
# Set the center frequency to 100 MHz
center_freq = 100e6 # Hz
num_samps = 10000 # number of samples returned per call to rx()

sdr = adi.Pluto('ip:192.168.2.1')
# Set the gain to 70 dB, automatic gain control turned off.
'''
Fixed vs automatic gain:
Automatic gain control (AGC) makes sure the singla level is -12dBFS.
- Makes sure the output power level is constant.

AGC:
- Fast attack: reacts quickly to changing signals
- Slow attack: reacts slowly to changing signals
'''
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 70.0 # dB
sdr.rx_lo = int(center_freq)
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate) # filter width, just set it to the same as sample rate for now
sdr.rx_buffer_size = num_samps

samples = sdr.rx() # receive samples off Pluto
print(samples[0:10])
print(len(samples))

'''
In order to check the current gain level:
'''

sdr.gain_control_mode_chan0 = "fast_attack"

# Calculate the average power of the signal
avg_pwr = np.mean(np.abs(samples)**2)