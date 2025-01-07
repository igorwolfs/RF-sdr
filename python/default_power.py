#! TEST: https://pysdr.org/content/pluto.html


import numpy as np
import math
import adi
import time
# Set the sample rate to 1 MHz
sample_rate = 1e6 # Hz
# Set the center frequency to 100 MHz
center_freq = 915e6 # Hz
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
sdr.rx_hardwaregain_chan0 = 0.0 # dB
sdr.rx_lo = int(center_freq)
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate) # filter width, just set it to the same as sample rate for now
sdr.rx_buffer_size = num_samps

for i in range(10):
    print(f"INDEX: <{i}>")
    samples = sdr.rx() # receive samples off Pluto
    rssi = sdr._ctrl.find_channel('voltage0').attrs['rssi'].value
    avg_pwr = np.mean(np.abs(samples)**2)
    log_pwr = 20*math.log(avg_pwr)
    print(f"log: {log_pwr} pwr: {avg_pwr}")
    print(f"rssi: {rssi}")
    print(f"------------")

sdr.rx_hardwaregain_chan0 = 0
# Calculate the average power of the signal
avg_pwr = np.mean(np.abs(samples)**2)


'''
# RSSI calculation (UG-570)
Is typically within 2 dB of the expected value.
NOTE: it is by default a relative, not an absolute value.

## RSSI Absolute value retrieval
In order to determine the absolute value of the RSSI (e.g.: in dBm)
- Inject a signal into the antenna port
- Read the RSSI word
- Generate a correction factor that corrects the RSSI.

## RSSI Gain Step calibration
Necessary for greater accuracy (0.25 dB precision)
'''