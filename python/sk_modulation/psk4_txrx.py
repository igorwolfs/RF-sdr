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
'''
### TX-bandwidth necessity:
The energy of the signal is spread around 914.5 MHz until 915.15 MHz
    - Indicated by the tx_rf_bandwidth
    - Indicates how long each symbol will be transmitted
The tx_lo frequency specifies the frequency of the local oscillator variable, which determines the carrier wave
    - In our case it is 915 MHz
'''
sdr.tx_rf_bandwidth = int(sample_rate)
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -20 # Tx power, valid range is -90 to 0 dB

# Create transmit waveform (QPSK, 16 samples per symbol)
num_symbols = 1000
# Create 1000 random numbers between 0 and 3
x_int = []
for i in range(int(num_symbols / 4)):
    x_int.append([0, 2, 1, 3])
x_int = np.asarray(x_int)
'''
 Create the PSK Phase-shifts:
 - Of the 1000 samples, some samples will be shifted by 45, 135, 225, 315 degrees.
 - Convert them to radians
'''
x_degrees = x_int*360/4.0 + 45
x_radians = x_degrees*np.pi/180.0

# this produces our QPSK complex symbols
'''
Equations involved in mixing:
s(t) = i(t) + q(t), exp(j*pi*f_lo*t) = cos(2*pi*f_lo*t) + j*sin(2*pi*f_lo*t)
the signal becomes 
Re(s(t) * exp(j*2*pi*f_lo*t))
= i(t) * cos(2*pi*f_lo*t) + q(t) * j*sin(2*pi*f_lo*t)
- Through which we modulate the phase as well as the amplitude
    - Amplitude is sqrt(i**2+Q**2), phase is arctan(q/i)

NOTE:
- Our DAC generates samples (so Q and I) once every MHz.
    - This generated sample stays the same for 1 us.
- This generated sample gets multiplied with our carrier wave, real part is filtered out using analog circuitry.
- Then it gets transmitted.
'''

x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians)

# Show the phase-shift modulated symbols
x_symbols_u = np.unique(x_symbols)
plt.plot(np.real(x_symbols_u), np.imag(x_symbols_u), '.')

plt.xlabel("Imag")
plt.ylabel("Real")

plt.grid(True)
plt.savefig(os.path.join(Plot_Path, 'psk.png'))
plt.show()


# 16 samples per symbol 
samples = np.repeat(x_symbols, 32)
# plt.plot(np.real(rx_samples[::10000]), label="real")
# plt.plot(np.imag(rx_samples[::10000]), label="imag")
# Plot the real part in the first subplot
fig, axs = plt.subplots(2)
axs[0].plot(np.real(samples[5000:5500]), label="Real", color='blue')
axs[1].plot(np.imag(samples[5000:5500]), label="Imaginary", color='orange')

plt.savefig(os.path.join(Plot_Path, 'psk_tx_t.png'))
plt.show()


samples *= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs
# Start the transmitter
sdr.tx_cyclic_buffer = True # Enable cyclic buffers


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

sdr.tx(samples) # start transmitting

# Clear buffer just to be safe
for i in range (0, 10):
    raw_data = sdr.rx()

# Receive samples
'''
Main question here: 
- What are we receiving?

'''
rx_samples = sdr.rx()

'''
### Demodulation
srx(t) = I(t) * cos(2*pi*fc*t) - Q(t) * sin(2*pi*fc*t)

- fc: carrier frequency
- It, Q(t): baseband in-phase and quadrature signals

then srx(t) * cos(2*pi*fc*t) = I(t) * pow2(cos(2*pi*fc*t)) - Q(t) * sin(2*pi*fc*t) * cos(2*pi*fc*t)
This leads to
- srx(t) * cos(2*pi*fc*t) = I(t) / 2 + I(t) * cos(4*pi*fc*t) / 2 - Q(t)*sin(4*pi*fc*t) / 2
Which we run through a low pass filter and multiply by 2, resulting in:
- I(t)

Multiplying the same srx(t) with (-sin(2*pi*fc*t)) gives us Q(t)
'''
print(f"{np.shape(rx_samples)}")
print(f"{np.shape(rx_samples[::1000])}")

# Stop transmitting
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

# Plot the real part in the first subplot
axs[0].plot(np.real(rx_samples[5000:5500]), label="Real", color='blue')
axs[1].plot(np.imag(rx_samples[5000:5500]), label="Imaginary", color='orange')
plt.savefig(os.path.join(Plot_Path, 'psk_rx_t.png'))


# Plot freq domain
fig, axs = plt.subplots(2)
axs[0].plot(f/1e6, psd_dB)
plt.savefig(os.path.join(Plot_Path, 'psk_rx_f.png'))
plt.show()

avg_pwr = np.mean(np.abs(rx_samples)**2)
print(f"average power: {20*math.log(avg_pwr)}")

'''
Demodulation of PSK (Phase Shift Keying)
- Achieved through abs(fft(rx_samples))**2
- So probably voltage**2
'''
# Decode the symbols, given you know it's phase-modulated
# We receive a waveform which is the same every 1 us
# When it changes, there is a sudden phase-change in the waveform
# Every-time this phase-change occurs, there is a new symbol being sent
# Main question is how do you detect a phase-shift in the frequency domain?


# Getting the cosine of the phase-shift can be achieved by 
# elementwise multiplication of the 2 signals
# dividing them by their multiplied RMS.


# If we know each signal is 1 uS long, and there are 4 phases encoded, we can just convolve each uS of samples with 