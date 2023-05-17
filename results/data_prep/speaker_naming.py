import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def getSpeakerDataIndexes(time, onset, duration):
    t1 = onset
    t2 = onset + duration
    i1 = np.argmin(np.abs(time - t1))
    i2 = np.argmin(np.abs(time - t2))
    return i1, i2

fileName = "Why_We_Will_NEVER_Have_Kids__Trash_Taste_129_HYitcJenxMA.wav"
rate, data = wav.read("../data/"+fileName)
print(data.shape)
print(rate)
length = data.shape[0] / rate
time = np.linspace(0., length, data.shape[0])
i1,i2 = getSpeakerDataIndexes(time, 0.498, 6.953)
print(i1,i2)
plt.plot(time[i1:i2], data[i1:i2,0], label="left")
plt.plot(time[i1:i2], data[i1:i2,1], label="right")
plt.legend()
plt.show()
f, t, Sxx = signal.spectrogram(data[i1:i2,0], rate)
plt.pcolormesh(t, f, Sxx)
print(Sxx.shape)
print(Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()