import numpy as np
import adi

sample_rate = 1e6 # Hz
center_freq = 915e6 # Hz

sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

# filter cutoff, just set it to the same as sample rate
sdr.tx_rf_bandwidth = int(sample_rate)
sdr.tx_lo = int(center_freq)
# Set the gain to -50 dB (range -90 -> 0 dB)
sdr.tx_hardwaregain_chan0 = -50

N = 10000 # number of samples to transmit at once
t = np.arange(N)/sample_rate
samples = 0.5*np.exp(2.0j*np.pi*100e3*t) # Simulate a sinusoid of 100 kHz, so it should show up at 915.1 MHz at the receiver
# Scale them between -2**14 -> 2**14, according to DAC requirements
samples *= 2**14

# Transmit our batch of samples 100 times, so it should be 1 second worth of samples total, if USB can keep up
for i in range(100):
    sdr.tx(samples) # transmit the batch of samples once