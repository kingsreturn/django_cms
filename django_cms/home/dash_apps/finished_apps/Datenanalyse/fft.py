import numpy as np
import matplotlib.pyplot as plt
def signal_samples(t):
    return np.sin(1 * np.pi * t) + np.sin(2 * np.pi * t) + np.sin(4 * np.pi * t)

def timesampling():
    sampling = 1000
    startpoint = 0
    endpoint = 100
    time = np.linspace(startpoint,endpoint,sampling)
    return time

def frequenzsampling(time):
    return np.sin(1 * np.pi * time) + np.sin(2 * np.pi * time) + np.sin(4 * np.pi * time)


B = 5.0
f_s = 2 * B
delta_f = 0.01
N = int(f_s / delta_f)
T = N / f_s
print(N)

time = timesampling()
#print(time)
f_t = frequenzsampling(time)

fig, axes = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
axes[0].plot(time, f_t)
axes[0].set_xlabel("time (s)")
axes[0].set_ylabel("signal")
axes[1].plot(time, f_t)
axes[1].set_xlim(0, 5)
axes[1].set_xlabel("time (s)")
plt.show()
#print(f_t)

from scipy import fftpack
F = fftpack.fft(f_t)
f = fftpack.fftfreq(N, 1.0/f_s)
mask = np.where(f >= 0)
fig, axes = plt.subplots(3, 1, figsize=(8, 6))

axes[0].plot(f[mask], np.log(abs(F[mask])), label="real")
axes[0].plot(B, 0, 'r*', markersize=10)
axes[0].set_ylabel("$\log(|F|)$", fontsize=14)

axes[1].plot(f[mask], abs(F[mask])/N, label="real")
axes[1].set_xlim(0, 2.5)
axes[1].set_ylabel("$|F|$", fontsize=14)

axes[2].plot(f[mask], abs(F[mask])/N, label="real")
axes[2].set_xlabel("frequency (Hz)", fontsize=14)
axes[2].set_ylabel("$|F|$", fontsize=14)
plt.show()