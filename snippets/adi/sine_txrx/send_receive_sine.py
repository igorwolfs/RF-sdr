import sys, os, shutil
from pathlib import Path, PurePath

## PLOT FOLDER SAVE
file_name = Path(__file__).parts[-1].strip(".py")
currDir = Path(__file__).parents[0]
Plot_Path = os.path.join(currDir, file_name)
if not (os.path.exists(Plot_Path)):
    os.mkdir(Plot_Path)
else:
    shutil.rmtree(Plot_Path)
    os.mkdir(Plot_Path)
		

import numpy as np
import adi, math
import matplotlib.pyplot as plt


##############################################################
######################### SETTINGS ###########################
##############################################################

pure_sine = True

sample_rate = 1e6 # Hz
center_freq = 915e6 # Hz
num_samps = 100000 # number of samples per call to rx()

sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

###########################################################################################################################
#                                                                                                                         #
############################################## TX CONFIGURATION ###########################################################
#                                                                                                                         #
###########################################################################################################################

# Config Tx
sdr.tx_rf_bandwidth = int(sample_rate)
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -20 # Tx power, valid range is -90 to 0 dB

# Create transmit waveform (QPSK, 16 samples per symbol)
sine_freq = 25e3

'''
We have to generate the samples, so that at a sample_rate of 1 MHz we get a sine-frequency of 50 Hz.
- Distance between samples in time is 1/sample_rate
- Create a sine with this sample rate by multiplying this with the sine frequency
'''
t_in = np.arange(0, 10, 1/sample_rate)
if (pure_sine):
    samples_tx = np.sin(t_in * 2 * np.pi * sine_freq)
else:
    # Phase shift the signal by 45 degrees (arctan(1))
    samples_tx = np.sin(t_in * 2 * np.pi * sine_freq) + 1j*np.cos(t_in*2*np.pi*sine_freq)


fig, axs = plt.subplots(2)
axs[0].plot(np.real(samples_tx[5000:5500]), label="Real", color='blue')
axs[1].plot(np.imag(samples_tx[5000:5500]), label="Imaginary", color='orange')
plt.savefig(os.path.join(Plot_Path, 'sine_tx_t.png'))

samples_tx *= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs
# Keeps transmitting the signal
sdr.tx_cyclic_buffer = True 

###########################################################################################################################
#                                                                                                                         #
############################################## RX CONFIGURATION ###########################################################
#                                                                                                                         #
###########################################################################################################################

'''
### RX-bandwidth necessity
- rx_lo: set the receiving oscillator
- rx_rf_bandwidth: set the receiving bandwidth
    - The signal is multiplied with the carrier frequency
    - Then a low-pass filter is passed over it
    - Then we are left with a 1 MHz signal of i(t) and q(t)
'''
sdr.rx_lo = int(center_freq)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 0.0 # dB, increase to increase the receive gain, but be careful not to saturate the ADC

sdr.tx(samples_tx) # start transmitting

# Clear buffer just to be safe
for i in range (0, 10):
    raw_data = sdr.rx()

rx_samples = sdr.rx()
sdr.tx_destroy_buffer()


# Calculate fft of the signal
fft_transformed = np.fft.fft(rx_samples)
# Shifts zero frequency component to the center of the spectrum
fft_shifted = np.fft.fftshift(fft_transformed)
# Calculate power spectral density (sum of squares of frequency components)
psd = np.abs(fft_shifted)**2
psd_dB = 10*np.log10(psd)
f = np.linspace(sample_rate/-2, sample_rate/2, len(psd))

# Plot time domain
fig, axs = plt.subplots(2)
axs[0].plot(np.real(rx_samples[5000:5500]), label="Real", color='blue')
axs[1].plot(np.imag(rx_samples[5000:5500]), label="Imaginary", color='orange')
plt.savefig(os.path.join(Plot_Path, 'sine_rx_t.png'))


# Plot freq domain
fig, axs = plt.subplots(1)
idx_max = np.where(psd_dB == np.max(psd_dB))

axs.plot(f/1e6, psd_dB)
axs.set_title(f"Max freq: {f[idx_max] / 1e3} kHz")
plt.savefig(os.path.join(Plot_Path, 'sine_rx_f.png'))

avg_pwr = np.mean(np.abs(rx_samples)**2)
print(f"average power: {20*math.log(avg_pwr)}")
