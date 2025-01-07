import numpy as np
import adi
import matplotlib.pyplot as plt
import time

# Each sample is 4 bytes
# USB2.0 max is 17 MB/s (iio_readdev -n 192.168.2.1 -b 100000 cf-ad9361-lpc | pv > /dev/null)
# So 17 / 4 = 4.25e6 samples/s approximately
sample_rate = 4.6e6 # Hz
center_freq = 2000e6 # Hz
samples_per_buffer = 1024*128
test_duration_seconds = 20

sdr = adi.Pluto("ip:192.168.2.1")

sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
sdr.rx_lo = int(center_freq)
sdr.rx_buffer_size = samples_per_buffer # this is the buffer the Pluto uses to buffer samples
#sdr.rx_enabled_channels = [0]
start_time = time.time()
end_time = start_time

i = 0
while (end_time - start_time < test_duration_seconds):
  samples = sdr.rx() # receive samples off Pluto
  i = i + 1
  end_time = time.time()
print(i/test_duration_seconds,' loops per second')
print('seconds elapsed:', end_time - start_time)
print('Samples read per second: ',(samples_per_buffer*i)/test_duration_seconds)