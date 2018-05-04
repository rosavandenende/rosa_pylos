#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 13:54:29 2018

@author: rosavandenende
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 11:49:00 2018

@author: rosavandenende
"""

#In dit document wordt een bandpass filter toegepast. Vervolgens wordt er een histogram gemaakt van elk stuk van de frequencies. Nu toegepast op de nieuwe data. 



import wave, struct
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, lfilter


def main(n):
    waveFile = wave.open("201650198.180129090002.wav", "r")
    length = waveFile.getnframes()
    sampling_rate = waveFile.getframerate()
    time_series = []
    print   (waveFile.getparams())
    
    for i in range(0,n):
        waveFile.setpos(i)
        waveData = waveFile.readframes(1)
        sample_point = struct.unpack("<h", waveData)
        time_series.append(sample_point[0])
   
    return time_series, sampling_rate
    
def butter_lowpass(cutoff, sampling_rate, order=5):
    nyq = 0.5 * sampling_rate
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, sampling_rate, order=5):
    b, a = butter_lowpass(cutoff, sampling_rate, order=order)
    y = lfilter(b, a, data)
    return y

def butter_highpass(cutoff, sampling_rate, order=5):
    nyq = 0.5 * sampling_rate
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, sampling_rate, order=5):
    b, a = butter_highpass(cutoff, sampling_rate, order=order)
    y = lfilter(b, a, data)
    return y

def butter_bandpass(lowcut, highcut, sampling_rate, order=5):
    nyq = 0.5 * sampling_rate
    low = lowcut/nyq
    high = highcut/nyq
    print (low, high)
    b, a = butter(order, [low, high], btype='band', analog=False)
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, sampling_rate, order=5):
    y = butter_lowpass_filter(data, highcut, sampling_rate, order)
    return butter_highpass_filter(y, lowcut, sampling_rate, order)

def PSD_using_scipy(ampl, fs):
    return signal.welch(ampl, fs, nperseg=1024, scaling= 'spectrum')


f, spectrum = PSD_using_scipy(main(100000)[0],main(100000)[1])
t = np.arange(len(main(100000)[0]))
time_series_filtered1= butter_bandpass_filter(main(100000)[0],1e3,10e3, main(100000)[1],order = 5)
time_series_filtered2= butter_bandpass_filter(main(100000)[0],10e3,25e3, main(100000)[1],order = 5)
time_series_filtered3= butter_bandpass_filter(main(100000)[0],25e3,50e3, main(100000)[1],order = 5)
time_series_filtered4= butter_bandpass_filter(main(100000)[0],1e3,50e3, main(100000)[1],order = 5)

f, spectrum_filtered = PSD_using_scipy(time_series_filtered4,main(100000)[1])
t1 = np.arange(len(time_series_filtered1))
t2 = np.arange(len(time_series_filtered2))
t3 = np.arange(len(time_series_filtered3))
t4 = np.arange(len(time_series_filtered4))

var1 = np.var(time_series_filtered1)
var2 = np.var(time_series_filtered2)
var3 = np.var(time_series_filtered3)
var4 = np.var(time_series_filtered4)
mean1 = np.mean(time_series_filtered1)
mean2 = np.mean(time_series_filtered2)
mean3 = np.mean(time_series_filtered3)
mean4 = np.mean(time_series_filtered4)
print (var1,var2,var3,var4)
print (mean1,mean2,mean3,mean4)


#Histograms of the amplitude 
def plot_histampl():
    plt.figure()
    plt.rcParams["figure.figsize"] = [24,9]
    plt.subplot(1,4,1)
    plt.hist(time_series_filtered1,bins=100000)
    plt.grid(True)
    plt.title("n=100 000, frequency 1 - 10 kHz")
    plt.xlim(-70,70)
    plt.xlabel("Amplitude")
    plt.ylabel("Nr of samples")
    plt.subplot(1,4,2)
    plt.hist(time_series_filtered2,bins=100000)
    plt.grid(True)
    plt.title("n=100 000, frequency 10 - 25 kHz")
    plt.xlim(-40,40)
    plt.xlabel("Amplitude")
    plt.ylabel("Nr of samples")
    plt.subplot(1,4,3)
    plt.hist(time_series_filtered3,bins=100000)
    plt.grid(True)
    plt.title("n=100 000, frequency 25 -50 kHz")
    plt.xlim(-20,20)
    plt.xlabel("Amplitude")
    plt.ylabel("Nr of samples")
    plt.subplot(1,4,4)
    plt.hist(time_series_filtered4,bins=100000)
    plt.grid(True)
    plt.title("n=100 000, frequency 1 - 50 kHz")
    plt.xlim(-70,70)
    plt.xlabel("Amplitude")
    plt.ylabel("Nr of samples")
    plt.show()
    


def plot_ADC(filtered):
    plt.rcParams["figure.figsize"]=[16,6]
    time_series = main(100000)[0]
    if filtered == False:
        plt.plot(t,time_series)
        plt.title("Ongefilterd")
    if filtered == True:
        plt.plot(t4,time_series_filtered4)
        plt.title("Gefilterd")
    plt.xlabel("sample nr")
    plt.ylabel("ADC")
    plt.grid(True)
    plt.show()
    
    
def plot_PSD(filtered):
    plt.rcParams["figure.figsize"]=[16,6]
    if filtered == False:
        plt.loglog(f,spectrum)
        plt.title("Ongefilterd")
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("PSD [ADC/$\sqrt{Hz}$]")
     
    if filtered == True:
        plt.loglog(f,spectrum_filtered)
        plt.title("Gefilterd")
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("PSD [ADC/$\sqrt{Hz}$]")
    plt.grid(True)
    plt.show()

plot_histampl()
plot_ADC(False)
plot_ADC(True)    
plot_PSD(False)
plot_PSD(True)
    


print ("Hoera")
