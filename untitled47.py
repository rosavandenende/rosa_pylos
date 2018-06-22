#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 16:04:19 2018

@author: chip
"""
#in this file: plotting the ADC of part of filtered signal
#basic stufffffffff

#21 06



import wave, struct
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, lfilter
import glob 
from datetime import datetime,timedelta
import pandas as pd 
import matplotlib.dates as mdates


def daterange():
    dateandtime_list = []
    deltatime = timedelta(minutes =2)
    dateandtime = datetime(year=2018,month=1,day=29,hour=9,minute=21,second=51)
    for i in range(0,59*30):
        dateandtime += deltatime
        dateandtime_list.append(dateandtime)
    print len(dateandtime_list)
    dateandtime_list = date2num(dateandtime_list) 
    print len(dateandtime_list),'r'
    return dateandtime_list

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

def main( c,d,a,b):
    file_list = sorted(glob.glob("/media/My Passport/Pylos_data/Py1-201650198/*.wav")) 
    time_series = []
    triggered = 0
    trigger_full = 0 
    full_list = []
    for j in range(c,d):
        waveFile = wave.open(file_list[j],"r")
        for i in range(a,b):
            waveFile.setpos(i)
            waveData = waveFile.readframes(1)
            sample_point = struct.unpack('<h',waveData)
            time_series.append(sample_point[0])
      
    time_series_filtered = butter_bandpass_filter(time_series,1e3,40e3,144000,order=5) 
    time_series_filtered = time_series_filtered[500:]
    sigma = np.std(time_series_filtered)
    for l in range(0,len(time_series_filtered)):
        if time_series_filtered[l] >= 5*sigma:
            triggered += 1
            print(l)
            if l > 0 and l < len(time_series_filtered):
                if (time_series_filtered[l] > time_series_filtered[l-1]) and (time_series_filtered[l] > time_series_filtered[l+1]):
                    trigger_full += 1
                    full_list.append(time_series_filtered[l])
                else: 
                    full_list.append(0)
        else:
            full_list.append(0)
                    
            
                    
#    print(np.where(time_series_filtered >= 5*sigma))
    print (sigma)
    print (triggered)
    print (trigger_full)
    print (len(full_list))
    time = np.linspace(0,120000,len(time_series_filtered))
    sigma_line = [5*sigma for i in range(len(time_series_filtered))]

    
    plt.rcParams["figure.figsize"] = [12,8]
    plt.rcParams["agg.path.chunksize"] = 10000       
    plt.plot(time,time_series_filtered,"-o")
    plt.plot(time,sigma_line,"r--")
    plt.scatter(time,full_list,color = "green",s = 8)
    plt.ylabel("ADC")
    plt.xlabel("Time (milli seconds)")
    plt.grid(True)

    plt.show()
    
main(50,51,360*144000,480*144000)