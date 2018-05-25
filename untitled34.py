#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 22 14:07:51 2018

@author: rosavandenende
"""

#NAV (telefoon)gesprek: bepaal 1 sigma van het hele gefilterde signaal. 


import wave, struct
from math import *
import numpy as np
import numpy.fft as fft
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

def main_trigger(n,low_cut,high_cut):
    file_list = glob.glob("/Volumes/My Passport/Pylos_data/Py1-201650198/*.wav")
    time_series = []
    triggered_list = []
    triggered = 0
   
    for i in file_list[7:8]:
        waveFile = wave.open(i,'r')
        sampling_rate = waveFile.getframerate()
        length = waveFile.getnframes()
        for j in range(0,int(n)):
            waveFile.setpos(j)
            waveData = waveFile.readframes(1)
            sample_point = struct.unpack("<h", waveData)
            time_series.append(sample_point[0]) 
        print (len(time_series))

    time_series_filtered = butter_bandpass_filter(time_series,low_cut,high_cut, sampling_rate,order = 5) 
    
    sigma_list = []
    sigma2_list = []
    teller = 0 
    teller_list = []
    for i in range(0,int(n)//int(120*144000)):                        #Hoe vaak moet sigma opnieuw bepaald worden --> elke twee minuten
        sigma = np.std(time_series_filtered[120*144000*i:120*144000*(i+1)])         #Sigma in lijst stoppen
        sigma_list.append(sigma)
        
        for element in time_series_filtered[120*144000*i:120*144000*(i+1)]:         #Voor elk element in dit stuk gefilterde lijst: is ie groter dan 5sigma?
            teller += 1
            if element >= (5*sigma):
                triggered += 1
                triggered_list.append(element)
                teller_list.append(teller)
       
    #als niet deelbaar door: 
    #je moet nog hebben: het stuk van i+1*144000 tot n (einde)
        
#    rest = (int(n)//int(144000)+1)*1440000          #Je moet nog het 'restgedeelte' hebben: van (n/144000 + 1)*144000 tot het einde
#    sigma = np.std(time_series_filtered[-rest:])
#    sigma_list.append(sigma)
#    print (sigma_list)
#    
    
    for sigma_value in sigma_list:              #Een lijst maken met de sigmavalues, evenvaak als de samples
        sigma2_list.extend([sigma_value]*(120*144000))
    print (len(sigma_list))
    print (len(sigma2_list))


    plt.rcParams["figure.figsize"] = [24,12]
    fig,ax = plt.subplots(2,1,sharex = False)
    ax[0].scatter(teller_list,triggered_list,s=10)
#    ax1.xlim(-400,len(time_series_filtered))
    ax[0].set_xlabel("sample number")
    ax[0].set_ylabel("ADC")
    ax[0].set_title("Triggered signals, amplitude > 5 * $\sigma$")
    ax[0].text(100000,350, "Number of triggers = %d" %triggered)
    
    #Offset time_series verwijderen
#    time_series0 = time_series - np.mean(time_series)
    ax[1].plot(range(len(time_series_filtered)),time_series_filtered,'green',linewidth = 0.7)
#    plt.plot(range(len(time_series0)),time_series0,linewidth = 0.7)
    ax[1].plot(range(len(time_series_filtered)),sigma2_list,'r--')
#    ax[1].axhline(y=5*sigma, color='r', linestyle='--')
    ax[1].set_title("Filtered signal (1-40 kHz)")
    ax[1].set_xlabel("sample number")
    ax[1].set_ylabel("ADC")

    plt.show()             
 
main_trigger(10*60*144000,1e3,40e3)

#Nog even over nadenken: het gefilterde signaal heeft geen offset