import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [16, 12]
plt.rcParams.update({"font.size": 18})

# Read csv file
df = pd.read_csv("pozyx_ranging_runs/data_2023-08-03_12-33-23_PRECISION.csv")
distances = df["Distance (mm)"]
timesteps = df["Timestep (ms)"]

# Plot the noisy raw data
plt.plot(timesteps, distances, color="c", label="Noisy")
# Create an xlim corresponding to the total number of entries in timesteps
xlim = np.arange(0, len(timesteps), 1)
plt.xlim(xlim[0], xlim[-1])
plt.xlabel("Timestep (ms)")
plt.ylabel("Distance (mm)")
plt.title("Raw Pozyx Data")
plt.legend()
plt.show()

dt = 0.016129032258064516  # Sampling period (s / sample)
# dt = 0.001

# Compute the Fast Fourier Transform (FFT)
n = len(timesteps)
print(f"fhat")
fhat = np.fft.fft(distances, n)  # Compute the FFT
print(f"PSD")
PSD = fhat * np.conj(fhat) / n  # Power spectrum (power per frequency)
print(f"freq")
freq = (1 / (dt * n)) * np.arange(n)  # Create x-axis of frequencies in Hz
L = np.arange(1, np.floor(n / 2), dtype="int")  # Only plot the first half of freqs

fig, axs = plt.subplots(2, 1)

plt.sca(axs[0])
plt.plot(timesteps, distances, color="c", label="Noisy")
plt.xlim(xlim[0], xlim[-1])
plt.xlabel("Timestep (ms)")
plt.ylabel("Distance (mm)")
plt.title("Raw Pozyx Data")
plt.legend()

plt.sca(axs[1])
print(f"freq[L]")
plt.plot(freq[L], PSD[L], color="c", label="Noisy")
plt.xlim(freq[L[0]], freq[L[-1]])
plt.xlabel("Frequency (Hz)")
print(f"Power")
plt.ylabel("Power")
plt.title("Power Spectrum")
plt.legend()

plt.show()
