#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 09:45:08 2018

@author: rosavandenende
"""

#In dit document: het bestand lezen voor alleen de eerste paar frames (maar dan wel het hele signaal, niet alleen de hoge). En histogram vd amplitude, kijken of dat een gaussische verdeling is 

import wave, struct
from math import *
import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt
from scipy import signal
import sys
import scipy.io.wavfile as wavfile
import os.path
from scipy.stats import norm


import wave

def PSD_using_scipy(ampl, fs):
    return signal.welch(ampl, fs, nperseg=1024, scaling= 'spectrum')

def main(argv):
    n = 10000
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
        
    t = np.arange(len(time_series))

    f, spectrum = PSD_using_scipy(time_series, sampling_rate)


    y_f = fft.fft(time_series)
    print (y_f[:100])
    print ("enter")
    print (np.abs(y_f[:100])//float(n))
    

    
    plt.hist(time_series,bins=1000)
    plt.grid(True)
    plt.title("Amplitudes n=10000")
    plt.xlabel("Amplitude")
    plt.ylabel("Nr of samples")
    plt.show()
    
    plt.plot(np.arange(0,5000), np.abs(y_f)[:5000])   
    plt.xlabel("Frequency [Hz]")                   
    plt.ylabel("FFT magnitude")
    plt.show()
    
    fig, (ax0, ax1) = plt.subplots(2, 1)
    plt.title("ADC and PSD for n = 10 000")
    ax0.plot(t, time_series,linewidth = 0.5)
    ax0.grid(True)
    ax0.set_xlabel('sample nr')
    ax0.set_ylabel('ADC')
    
    ax1.loglog(f, spectrum,linewidth = 0.5) 
    ax1.grid(True)
    ax1.set_xlabel('frequency [Hz]')
    ax1.set_ylabel('PSD [ADC/$\sqrt{Hz}$]')
    plt.rcParams["figure.figsize"] = [24,9]
    plt.subplots_adjust(hspace=0.4)
    plt.show()
      

if __name__ == '__main__':
    main(sys.argv)
    
print ("Hoera")