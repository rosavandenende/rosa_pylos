#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#In dit document wordt een bandpass filter toegepast. Vervolgens wordt er een histogram gemaakt van elk stuk van de frequencies. Nu toegepast op de nieuwe data. 

import wave, struct
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, lfilter

def main(n,plot):
    waveFile = wave.open("201650198.180129105957.wav", "r")
    length = waveFile.getnframes()
    sampling_rate = waveFile.getframerate()
    time_series = []
    print   (waveFile.getparams())
    
    for i in range(0,n):
        waveFile.setpos(i)
        waveData = waveFile.readframes(1)
        sample_point = struct.unpack("<h", waveData)
        time_series.append(sample_point[0])
    if plot == True:
        plt.plot(time_series,range(0,n))
        plt.xlabel("sample number")
        plt.ylabel("ADC")
        plt.show()
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


def plot_hist(n,plot):
    time_series_filtered = []
    mean = []
    sigma = []
    t = []
    filter_list = np.arange(1e3,51e3,1e3)
    for l in range(len(filter_list)-1):
        low_cut = filter_list[l]
        high_cut = filter_list[l+1]
        
        time_series_f = butter_bandpass_filter(main(n,False)[0],low_cut,high_cut, main(n,False)[1],order = 5)
        time_series_filtered.append(time_series_f)
        sigma.append(np.std(time_series_f))
        mean.append(np.mean(time_series_f))
        t.append(np.arange(len(time_series_f)))
        if plot == True:
            plt.hist(time_series_f,bins = 1000)
            plt.grid(True)
            plt.title("n=%d, f = %d-%d kHz " %(n,low_cut//1000,high_cut//1000))
            plt.xlabel("ADC")
            plt.ylabel("Nr of samples")
            plt.show()
    return(time_series_filtered, sigma, mean)

def plot_sigmafreq(n):
    sigma = plot_hist(n,False)[1]
    mean = plot_hist(n,False)[2]
    freq = np.arange(1e3,50e3,1e3)
    plt.scatter(freq,sigma,s=5)
    plt.ylabel("sigma")
    plt.xlabel("Frequency [Hz]")
    plt.title("Width of the Gaussian as function of the frequency, for n = %d" %n)
    print (sigma, "hello", mean)
    plt.show()
    #LET OP: NOG CHECKEN OF HET GEMIDDELDE VAN SIGMA MOET WORDEN AFGETROKKEN 

#f, spectrum = PSD_using_scipy(main(100000)[0],main(100000)[1])
#f, spectrum_filtered = PSD_using_scipy(time_series_filtered4,main(100000)[1])



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

#plot_ADC(False)
#plot_ADC(True)    
#plot_PSD(False)
#plot_PSD(True)
    
#plot_hist(10000,False)
plot_sigmafreq(10000)

print ("Hoera")
