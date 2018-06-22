#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 17:24:44 2018

@author: chip
"""


#in this file: saving sigma and triggered 
#but now for 50, 80



import wave, struct
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, lfilter
import glob 
from datetime import datetime,timedelta
import pandas as pd 
import matplotlib.dates as mdates

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

def PSD_using_scipy(ampl, fs):
    return signal.welch(ampl, fs, nperseg=1024, scaling= 'spectrum')


def main_trigger(a,b,c,low_cut,high_cut):
    print (datetime.now())
    file_list = sorted(glob.glob("/media/My Passport/Pylos_data/Py1-201650198/*.wav"))                    #Maakt een lijst met alle bestandsnamen uit het mapje
    time_series = []
    samples_per_sigma = 120 * 144000                                                                #Elke 120 seconden wordt sigma opnieuw bepaald
    sigma_list = []
    triggered = 0
    triggered_list = []
    
    
    
    #Making a list with the time values: 2 minutes are added 
#    date_list = []
    dateandtime_list = []
    dateandtime = datetime(year=2018,month=2,day=2,hour = 12, minute=59,second=9)
    deltatime = timedelta(minutes = 2)
    for i in range(0,c*(b-a)):
        dateandtime = dateandtime + deltatime
        dateandtime_list.append(dateandtime)
    print( "len of datetimelist", len(dateandtime_list))
    
    
    for i in file_list[a:b]:
        waveFile = wave.open(i,'r')
        sampling_rate = waveFile.getframerate()      
#       date_list.append(i)
        
        for startpoint in range(0,c):                                                  #hoeveel stukjes van 120 sec wil je
            for j in range(int(startpoint*samples_per_sigma),int((startpoint+1)*samples_per_sigma)):                       #deze is dus max 2 min                                
                waveFile.setpos(j)
                waveData = waveFile.readframes(1)
                sample_point = struct.unpack("<h", waveData)
                time_series.append(sample_point[0])
            time_series_filtered = butter_bandpass_filter(time_series,low_cut,high_cut, sampling_rate,order = 5) 
            print len(time_series_filtered)
#            time_series_filtered = time_series_filtered[500:]
 
            sigma = np.std(time_series_filtered)
            sigma_list.append(5*sigma)
            print (sigma)
            for element in time_series_filtered:         
                if element >= (5*sigma):
                   triggered += 1
            
                       
            triggered_list.append(triggered)
         
                  #Let op!! Hier is triggered_list de lijst met de HOEVEELHEDEN getriggerd, dus niet de getriggerede elementen
            time_series = []
            time_series_filtered = []
            triggered = 0
    np.savetxt("%i %i %i sigma and triggered" %(a,b,c),[sigma_list,triggered_list])

#    
#    plt.rcParams["figure.figsize"] = [16,10]
#    fig,ax = plt.subplots(2,1,sharex = True)
#    ax[0].scatter(dateandtime_list,sigma_list,s=10)
#    ax[0].set_xlabel("Date (y-m-d h:m)")
#    ax[0].set_ylabel("Noise level, 5$\sigma$")
#    ax[0].set_title("Noise level over time")
#    plt.subplots_adjust(hspace = 0.4)
#    ax[1].scatter(dateandtime_list,triggered_list,s=10)
#    ax[1].set_title("Number of triggered signals over time")
#    ax[1].set_xlabel("Date (y-m-d h:m)")
#    ax[1].set_ylabel("Number of triggers")
#    xfmt = mdates.DateFormatter("%d-%m-%y %H:%M")
#    ax[0].xaxis.set_major_formatter(xfmt)
#    plt.xticks(rotation = 45)
#    plt.savefig("%i %i %i 5sigma and triggered" %(a,b,c))
#    plt.show()
    
    print (datetime.now())

main_trigger(50,80,59,1e3,40e3)















