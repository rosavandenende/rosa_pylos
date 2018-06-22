#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 19:29:21 2018

@author: chip
"""

import numpy as np
from scipy import signal
from scipy.signal import butter, lfilter
import numpy.fft as fft
import matplotlib.pyplot as plt
import glob
import wave, struct




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
    b, a = butter(order, [low, high], btype='band', analog=False)
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, sampling_rate, order=5):
    y = butter_lowpass_filter(data, highcut, sampling_rate, order)
    return butter_highpass_filter(y, lowcut, sampling_rate, order)


def PSD_using_numpy(ampl, fs):
    spectrum = fft.fft(ampl)
    PSD = np.abs(spectrum)**2 * (2./(fs*len(spectrum)))
    freq = fft.fftfreq(len(spectrum),d=1./fs)
    plt.loglog(freq,PSD)
    plt.show()

def PSD_using_scipy(ampl, fs):
    return signal.welch(ampl, fs, nperseg=1024, scaling= 'spectrum')


def main(a,b,c,d):
    file_list = sorted(glob.glob("/media/My Passport/Pylos_data/Py1-201650198/*.wav")) 
    time_series = []
    for j in range(a,b):
        waveFile = wave.open(file_list[j],"r")
        for i in range(c,d):
            waveFile.setpos(i)
            waveData = waveFile.readframes(1)
            sample_point = struct.unpack('<h',waveData)
            time_series.append(sample_point[0])
    return time_series



#PSD_using_numpy(main(0,1,10000,50000),144000.)
tsf = butter_highpass_filter(main(0,1,10000,50000),1e3, 144000,order=5)
freq,spec = PSD_using_scipy(tsf,144000.)
plt.loglog(freq,spec)
plt.show()
