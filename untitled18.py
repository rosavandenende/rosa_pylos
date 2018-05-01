#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 11:49:00 2018

@author: rosavandenende
"""


#In dit document wordt een bandpass filter toegepast. Vervolgens wordt er een histogram gemaakt van elk stuk van de frequencies. Eigen methode, dus zonder EJ's lange run funcite
import wave, struct
import math
import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt
from scipy import signal
import sys
import os.path

from scipy.stats import norm
from scipy.signal import butter, lfilter


def main(n):
    waveFile = wave.open("pylos20180411.wav", "r")
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


#Histograms of the amplitude
figurehist = plt.figure()
plt.subplot(1,4,1)
plt.hist(time_series_filtered1,bins=10000)
plt.grid(True)
plt.title("n=100 000, frequency 1 - 10 kHz")
plt.xlim(-50,50)
plt.xlabel("Amplitude")
plt.ylabel("Nr of samples")
plt.subplot(1,4,2)
plt.hist(time_series_filtered2,bins=10000)
plt.grid(True)
plt.title("n=100 000, frequency 10 - 25 kHz")
plt.xlim(-10,10)
plt.xlabel("Amplitude")
plt.ylabel("Nr of samples")
plt.subplot(1,4,3)
plt.hist(time_series_filtered3,bins=10000)
plt.grid(True)
plt.title("n=100 000, frequency 25 -50 kHz")
plt.xlim(-10,10)
plt.xlabel("Amplitude")
plt.ylabel("Nr of samples")
plt.subplot(1,4,4)
plt.hist(time_series_filtered4,bins=10000)
plt.grid(True)
plt.title("n=100 000, frequency 1 - 50 kHz")
plt.xlim(-50,50)
plt.xlabel("Amplitude")
plt.ylabel("Nr of samples")
plt.show()
    
#ADC and PSD of unfiltered signal
time_series = main(100000)[0]
plt.rcParams["figure.figsize"] = [24,9]
fig, (ax0, ax1) = plt.subplots(2, 1)
plt.title("n = 100 000, unfiltered signal")
ax0.plot(t, time_series,linewidth = 0.3)
ax0.grid(True)
ax0.set_xlabel('sample nr')
ax0.set_ylabel('ADC')
    
ax1.loglog(f, spectrum,linewidth = 0.7) 
ax1.grid(True)
ax1.set_xlabel('frequency [Hz]')
ax1.set_ylabel('PSD [ADC/$\sqrt{Hz}$]')
plt.rcParams["figure.figsize"] = [24,9]
plt.subplots_adjust(hspace=0.4)
plt.show()
#ADC of filtered signal
plt.rcParams["figure.figsize"] = [24,9]
fig, (ax0, ax1) = plt.subplots(2, 1)
plt.title("n = 100 000, filtered signal 1-50 kHz")
ax0.plot(t4, time_series_filtered4,linewidth = 0.3)
ax0.grid(True)
ax0.set_xlabel('sample nr')
ax0.set_ylabel('ADC')
    
ax1.loglog(f, spectrum_filtered,linewidth = 0.7) 
ax1.grid(True)
ax1.set_xlabel('frequency [Hz]')
ax1.set_ylabel('PSD [ADC/$\sqrt{Hz}$]')
plt.rcParams["figure.figsize"] = [24,9]
plt.subplots_adjust(hspace=0.4)
plt.show()

print ("Hoera")
