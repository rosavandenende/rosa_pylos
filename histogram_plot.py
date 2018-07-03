#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 20:38:34 2018

@author: rosavandenende
"""

import wave, struct
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, lfilter
import glob 

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


def main(m,n,a,b,low_cut,high_cut):
    file_list = glob.glob("/Volumes/My Passport/Pylos_data/Py1-201650198/*.wav")                    #Maakt een lijst met alle bestandsnamen uit het mapje
    time_series = []
    for i in range(a,b):
        filename = file_list[i]
        waveFile = wave.open(filename,'r')
        sampling_rate = waveFile.getframerate()      
                                                #hoeveel stukjes van 120 sec wil je
        for j in range(int(m),int(n)):                 #deze is dus max 2 min                                
            waveFile.setpos(j)
            waveData = waveFile.readframes(1)
            sample_point = struct.unpack("<h", waveData)
            time_series.append(sample_point[0]) 
            
   
    time_series_filtered = butter_bandpass_filter(time_series,low_cut,high_cut, sampling_rate,order = 5) 
    plt.hist(time_series_filtered,bins=100000)
    plt.title("ADC-histogram of filtered signal, %s" %filename[-16:-4])
    
    plt.style.use('classic')
    plt.rcParams['font.size'] = 18
    plt.rcParams['font.family'] = 'serif'

    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 16
    plt.rcParams['figure.titlesize'] = 14

    plt.rcParams['legend.numpoints'] = 1

    plt.rcParams['figure.figsize'] = 6.4, 4.8
    plt.grid(True)
    plt.xlabel("Amplitude")
    plt.xlim(-50,50)
    plt.ylabel("Number of samples")
    plt.show()
 
main(144000*7080,144000*7082,1,2,1e3,40e3)