import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz

# Create a sample signal with two frequencies
fs = 500.0  # Sample rate (Hz)
t = np.arange(0, 1.0, 1 / fs)  # Time vector
signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(
    2 * np.pi * 120 * t
)  # Sum of 2 frequencies: 5 Hz and 120 Hz

# Design a Butterworth filter lowpass filter with a cutoff frequency of 10 Hz
# b, a = butter(N=6, Wn=10.0, btype='low', analog=False, output='ba', fs=fs)
b, a = butter(N=6, fs=fs, Wn=10.0, btype="low")

# Apply the filter to the signal
filtered_signal = lfilter(b, a, signal)

# Plot the original signal and the filtered signal
plt.figure()
plt.plot(t, signal, "b-", label="data")
plt.plot(t, filtered_signal, "g-", linewidth=2, label="filtered data")
plt.xlabel("Time [sec]")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()
plt.show()
