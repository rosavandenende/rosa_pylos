#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#In dit document wordt een bandpass filter toegepast. Vervolgens wordt er een histogram gemaakt van elke frequency.

import wave, struct
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, lfilter
import matplotlib.patches as patches



    
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

def main(n,plot,filename):
    waveFile = wave.open(filename, "r")
    length = waveFile.getnframes()
    sampling_rate = waveFile.getframerate()
    time_series = []
    
    for i in range(0,int(n)):
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

def plot_hist(n,plot,filename):
    time_series_filtered = []
    mean = []
    sigma = []
    t = []
    filter_list = np.arange(1e3,41e3,1e3)
#    fig = plt.figure()
#    fig.subplots_adjust(hspace=0.4,wspace=0.4)
    for l in range(len(filter_list)-1):
        low_cut = filter_list[l]
        high_cut = filter_list[l+1]
        
        time_series_f = butter_bandpass_filter(main(n,False,filename)[0],low_cut,high_cut, main(n,False,filename)[1],order = 5)
        time_series_filtered.append(time_series_f)
        sigma.append(np.std(time_series_f))
        mean.append(np.mean(time_series_f))
        t.append(np.arange(len(time_series_f)))
    if plot == True:
#            ax = fig.add_subplot(10,5,l+1)
#            ax.hist(time_series_f,bins = 1000)
        plt.hist(time_series_f,bins = 1000)
        plt.grid(True)
        plt.title("n=%d, f = %d-%d kHz " %(n,low_cut//1000,high_cut//1000))
        plt.xlabel("ADC")
        plt.ylabel("Nr of samples")
        plt.show()
    return(time_series_filtered, sigma, mean)


def plot_sigmafreq(n,filename):
    sigma = plot_hist(n,False,filename)[1]
    mean = plot_hist(n,False,filename)[2]
    freq = np.arange(1e3,40e3,1e3)
    print (len(sigma),len(freq))
    plt.scatter(freq,sigma,s=10)
#   plt.plot(freq,1/(freq**2),'red')
    plt.ylabel("Sigma")
    plt.xlabel("Frequency [Hz]")
#    plt.title("Width of the Gaussian as function of the frequency, %s" %filename[-16:-4])
    print (sigma, "hello", mean)
    plt.show()
    #LET OP: NOG CHECKEN OF HET GEMIDDELDE VAN SIGMA MOET WORDEN AFGETROKKEN 

plot_sigmafreq(1e6,"201650198.180220085641.wav")













def plot_ADC(n,filtered):
    plt.rcParams["figure.figsize"]=[16,6]
    time_series = main(n,False)[0]
    time_series_filtered = butter_bandpass_filter(main(n,False)[0],1e3,50e3, main(n,False)[1],order = 5)
    if filtered == False:
        plt.plot(range(0,n),time_series)
        plt.title("Unfiltered signal, n=%d" %n)
    if filtered == True:
        plt.ylim(-20,20)
        plt.plot(range(0,n),time_series_filtered)
        plt.title("Filtered signal, n=%d" %n)
    plt.xlabel("sample nr")
    plt.ylabel("ADC")
    plt.grid(True)
    plt.show()
       
def plot_PSD(n,filtered):
    plt.rcParams["figure.figsize"]=[16,6]
    if filtered == False:
        f,spectrum = PSD_using_scipy(main(n,False)[0],main(n,False)[1])
        plt.title("Unfiltered signal, n=%d" %n)
        
    if filtered == True:
        time_series_filtered = butter_bandpass_filter(main(n,False)[0],1e3,50e3, main(n,False)[1],order = 5)
        f, spectrum = PSD_using_scipy(time_series_filtered,main(n,False)[1])
        #CHECKEN OF DE SAMPLE RATE NOG WEL HETZELFDE IS VOOR HET GEFILTERDE SIGNAAL
        plt.title("Filtered signal, n=%d" %n)
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("PSD [ADC/$\sqrt{Hz}$]")
    plt.loglog(f,spectrum)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("PSD [ADC/$\sqrt{Hz}$]")
    plt.grid(True)
    plt.show()


#
#plot_ADC(10000,False)
#plot_ADC(10000,True)    
#plot_PSD(10000,False)
#plot_PSD(10000,True)
#plot_sigmafreq(10000)
#plot_hist(10000,True)
#print ("Hoera")


def plot_meansigma():
    
    freq = np.arange(1e3,50e3,1e3)
    sigma=plot_hist(10000,False)[1]
    mean = plot_hist(10000,False)[2]
    sigma3 = []
    for i in sigma:
        sigma3.append(3*i)
    plt.plot(freq,mean)
    plt.plot(freq,sigma3,'r')
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("ADC")
    red_patch = patches.Patch(color = 'red', label = '3 * sigma')
    blue_patch = patches.Patch(color = 'blue', label = 'Mean')
    plt.legend(handles = [red_patch, blue_patch])
    plt.show()
    
#plot_meansigma()

