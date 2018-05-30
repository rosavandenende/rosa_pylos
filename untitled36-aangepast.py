#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 14:59:37 2018

@author: chip
"""

import wave, struct
import numpy as np
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


def main_trigger(a,b,c,low_cut,high_cut):
    file_list = glob.glob("/media/My Passport/Pylos_data/Py1-201650198/*.wav")                    #Maakt een lijst met alle bestandsnamen uit het mapje
    time_series = []
    samples_per_sigma = 120 * 144000                                                                #Elke 120 seconden wordt sigma opnieuw bepaald
    sigma_list = []
    sigma2_list = []
    triggered = 0
    triggered_list = []
#    teller = 0 
#    teller_list = []
   
    for i in file_list[a:b]:
        waveFile = wave.open(i,'r')
        sampling_rate = waveFile.getframerate()      

           
        for startpoint in range(0,c):                                                  #hoeveel stukjes van 120 sec wil je
            for j in range(int(startpoint*samples_per_sigma),int((startpoint+1)*samples_per_sigma)):                       #deze is dus max 2 min                                
                waveFile.setpos(j)
                waveData = waveFile.readframes(1)
                sample_point = struct.unpack("<h", waveData)
                time_series.append(sample_point[0]) 
                
            time_series_filtered = butter_bandpass_filter(time_series,low_cut,high_cut, sampling_rate,order = 5) 
            sigma = np.std(time_series_filtered)
            sigma_list.append(5*sigma)
            print (sigma)    
            for element in time_series_filtered:         
#                teller += 1 
                if element >= (5*sigma):
                    triggered += 1
            triggered_list.append(triggered)
         
                  #Let op!! Hier is triggered_list de lijst met de HOEVEELHEDEN getriggerd, dus niet de getriggerede elementen
#                    teller_list.append(teller) 
            print (triggered)
            time_series = []
            time_series_filtered = []
            triggered = 0
                
    print (len(triggered_list))
    print (len(sigma_list))
    print (triggered_list)
    print (sigma_list)
#    for sigma_value in sigma_list[:-1]:                                                               #Een lijst maken met de sigmavalues, evenvaak als de samples
#        sigma2_list.extend([5*sigma_value]*(samples_per_sigma)) 
#    sigma2_list.extend([5*sigma_list[-1]]*(rest_len))
     
#    np.savetxt("30050218_45_3.txt",(triggered_list,sigma_list))
    plt.rcParams["figure.figsize"] = [16,10]
    time = np.arange(1,2*c,2)

    fig,ax = plt.subplots(2,1,sharex = True)
    
    ax[0].scatter(time,sigma_list)
    ax[0].set_xlabel("Time (minutes)")
    ax[0].set_ylabel("Noise level, 5$\sigma$")
#    ax[0].set_title("Noise level over time, %s" %i[-15])
    plt.subplots_adjust(hspace = 0.4)
    ax[1].scatter(time,triggered_list)
#    ax[1].set_title("Number of triggered signals over time, %s" %i[-15])
    ax[1].set_xlabel("Time (minutes)")
    ax[1].set_ylabel("Number of triggers")
    plt.show()

main_trigger(4,5,20,1e3,40e3)