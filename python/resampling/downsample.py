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

##############################################################
######################### SETTINGS ###########################
##############################################################

lp_filter_enabled = True

##########################################################
######################### CODE ###########################
##########################################################

# Create sinuoidal signal, 12000 samples / second
sine_freq = 50 # Hz
sr_high = 12e3
sr_low = 1e3
duration = 10
t_high = np.arange(0, duration, 1/sr_high)
signal_high = np.sin(2 * np.pi * sine_freq * t_high)

# Add dirty sine frequency to check effect of LP-filter on frequency spectrum
dirty_sine_freq = 300+sr_low/2
signal_dirty = np.sin(2 * np.pi * t_high * dirty_sine_freq)
signal_high = np.add(signal_high, signal_dirty)



######################################################
################# FILTERING ##########################
######################################################

# Low-pass filter function to prevent aliasing
def low_pass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs  # Nyquist frequency
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)


# Pass through low-pass filter
'''
Bringing down the sample-rate reduces the nyquist frequency
- before: sr_high/2
- after: sr_low / 2
So any frequencies between [sr_low/2, sr_high/2] get aliased down between [DC, sr_low/2], since frequencies will fold back onto fa = |f - k*sr_new|
We have to get rid of those by using a low-pass filter with a cutoff at at-least the neq nyquist frequency (so sr_low/2)
NOTE: You could go even lower for signals that are positioned around the edge, but then you risk losing signal bandwidth.
'''
if (lp_filter_enabled):
    cutoff_freq = sr_low / 2  # Cutoff frequency for anti-aliasing (new nyquist frequency)
    signal_filtered = low_pass_filter(signal_high, cutoff_freq, sr_high)
else:
    signal_filtered = np.copy(signal_high)

#########################################################
################# DOWNSAMPLING ##########################
#########################################################

# Downsample the signal
downsample_factor = int(sr_high // sr_low)  # Compute downsampling factor
print(f"downsample-factor: {downsample_factor}")
signal_low = signal_filtered[::downsample_factor]  # Take every N-th sample
t_low = t_high[::downsample_factor]  # Downsampled time vector


# Plot original and downsampled signals
plt.figure(figsize=(12, 6))


######################################################
################# PLOTS ##############################
######################################################
plt_dur = 0.100 # s
plt.subplot(3, 1, 1)
plt_dur_1 = int(sr_high * plt_dur)
plt.plot(t_high[:plt_dur_1], signal_high[:plt_dur_1], label="Original Signal (1 kHz)")
plt.title("Original Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

# Upsampled signal
plt.subplot(3, 1, 2)
plt.plot(t_high[:plt_dur_1], signal_filtered[:plt_dur_1], label="Upsampled Signal (12 kHz)", color='orange')
plt.title("Upsampeld Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

# Upsampled and filtered signal
plt.subplot(3, 1, 3)
plt_dur_2 = int(sr_low * plt_dur)

plt.plot(t_low[:plt_dur_2], signal_low[:plt_dur_2], label="Upsampled Signal with LP filter (12 kHz)", color='red')
plt.title("Upsampeld Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.savefig(os.path.join(Plot_Path, 'downsampled_t.png'))
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
res_h = plot_spectrum(signal_high, sr_high)
plt.plot(res_h[0][:res_h[2]], res_h[1][:res_h[2]], label="Original Signal (12 kHz)")
plt.title("Original Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

# Upsampled signal
plt.subplot(3, 1, 2)
res_h_f = plot_spectrum(signal_filtered, sr_high)
plt.plot(res_h_f[0][:res_h_f[2]], res_h_f[1][:res_h_f[2]], label="Filtered signal (12 kHz)", color='orange')
plt.title("filtered Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

# Upsampled and filtered signal
plt.subplot(3, 1, 3)
res_l = plot_spectrum(signal_low, sr_low)
plt.plot(res_l[0][:res_l[2]], res_l[1][:res_l[2]], label="Downsampled signal (1 kHz)", color='red')
plt.title("Downsampled Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.savefig(os.path.join(Plot_Path, 'downsampled_f.png'))
plt.show()
