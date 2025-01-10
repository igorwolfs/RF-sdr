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
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, filtfilt

######################################################
################# FREQUENCY ##########################
######################################################

# Create sinuoidal signal, 12000 samples / second
sine_freq = 50 # Hz
sr_high = 12e3
sr_low = 1e3
duration = 10
t_high = np.arange(0, duration, 1/sr_high)
t_low = np.arange(0, duration, 1/sr_low)
signal_low = np.sin(2 * np.pi * sine_freq * t_low)
signal_high = np.zeros(int(duration * sr_high))


# Downsample the signal
upsample_factor = int(sr_high // sr_low)  # Compute downsampling factor
print(f"upsample-factor: {upsample_factor}")
signal_high[::upsample_factor] = signal_low  # Take every N-th sample



######################################################
################# FILTERING ##########################
######################################################

'''
# Using lfilter vs filtfilt
## filtfilt
Zero-phase filtering. So no phase-shfit during filtering.
Can only be used when the full signal is present.
## lfilter
Causal forward-in-time filtering. Adds delay depending on the frequency used.
'''
# Low-pass filter function to prevent imaging
def low_pass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs  # Nyquist frequency
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)

# def low_pass_filter(data, cutoff, fs, order=5):
#     nyquist = 0.5 * fs
#     normal_cutoff = cutoff / nyquist
#     b, a = butter(order, normal_cutoff, btype='low', analog=False)
#     return filtfilt(b, a, data)

# Pass through low-pass filter
cutoff_freq = sr_low / 2  # Cutoff frequency for anti-imaging
signal_filtered = low_pass_filter(signal_high, cutoff_freq, sr_high)

######################################################
################# PLOTS ##############################
######################################################

# Plot original and downsampled signals
plt.figure(figsize=(12, 6))

################# TIME PLOTS ##################
# Original signal
plt_dur = 0.100 # s
plt.subplot(3, 1, 1)
plt_dur_1 = int(sr_low * plt_dur)
plt.plot(t_low[:plt_dur_1], signal_low[:plt_dur_1], label="Original Signal (1 kHz)")
plt.title("Original Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

# Upsampled signal
plt.subplot(3, 1, 2)
plt_dur_2 = int(sr_high * plt_dur)
plt.plot(t_high[:plt_dur_2], signal_high[:plt_dur_2], label="Upsampled Signal (12 kHz)", color='orange')
plt.title("Upsampeld Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

# Upsampled and filtered signal
plt.subplot(3, 1, 3)
plt.plot(t_high[:plt_dur_2], signal_filtered[:plt_dur_2], label="Upsampled Signal with LP filter (12 kHz)", color='red')
plt.title("Upsampeld Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.savefig(os.path.join(Plot_Path, 'upsampled_t.png'))
plt.show()


################# FREQ PLOTS ##################
# Fourier Transform Function
def plot_spectrum(signal, fs):
    N = len(signal)  # Length of the signal
    freq = np.fft.fftfreq(N, 1/fs)  # Frequency axis
    fft_values = np.fft.fft(signal)  # Fourier Transform
    magnitude = np.abs(fft_values)  # Magnitude spectrum

    # Plot positive frequencies only
    half_N = N // 2
    return freq, magnitude, half_N


# Original signal
plt.subplot(3, 1, 1)
res_l = plot_spectrum(signal_low, sr_low)
plt.plot(res_l[0][:res_l[2]], res_l[1][:res_l[2]], label="Original Signal (1 kHz)")
plt.title("Original Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

# Upsampled signal
plt.subplot(3, 1, 2)
res_h = plot_spectrum(signal_high, sr_high)
plt.plot(res_h[0][:res_h[2]], res_h[1][:res_h[2]], label="Upsampled Signal (12 kHz)", color='orange')
plt.title("Upsampeld Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

# Upsampled and filtered signal
plt.subplot(3, 1, 3)
res_h_f = plot_spectrum(signal_filtered, sr_high)
plt.plot(res_h_f[0][:res_h_f[2]], res_h_f[1][:res_h_f[2]], label="Upsampled Signal with LP filter (12 kHz)", color='red')
plt.title("Upsampeld Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.savefig(os.path.join(Plot_Path, 'upsampled_f.png'))
plt.show()
