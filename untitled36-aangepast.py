#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 14:59:37 2018

@author: chip
"""

#in this document: plotting the noise level and the number of triggered signals over time. Nu proberen van elke twee minuten de eerste 500 samples eruit te gooien. 



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
    triggered5 = 0
    triggered6 = 0
    triggered7 = 0
    triggered8 = 0
    triggered9 = 0
    triggered5_list = []
    triggered6_list = []
    triggered7_list = []
    triggered8_list = []
    triggered9_list = []
    
    
    
    #Making a list with the time values: 2 minutes are added 
#    date_list = []
    dateandtime_list = []
    dateandtime = datetime(year=2018,month=1,day=29,hour = 9, minute=00,second= 02)
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
                   triggered5 += 1
                   if element >= (6*sigma):
                      triggered6 += 1
                      if element >= (7*sigma):
                       triggered7 += 1
                       if element >= (8*sigma):
                           triggered8 += 1
                           if element >= (9*sigma):
                               triggered9 += 1
                       
                       
            triggered5_list.append(triggered5)
            triggered6_list.append(triggered6)
            triggered7_list.append(triggered7)
            triggered8_list.append(triggered8)
            triggered9_list.append(triggered9)
    
         
                  #Let op!! Hier is triggered_list de lijst met de HOEVEELHEDEN getriggerd, dus niet de getriggerede elementen
            time_series = []
            time_series_filtered = []
            triggered5 = 0
            triggered6 = 0
            triggered7 = 0
            triggered8 = 0
            triggered9 = 0
    np.savetxt("%i %i %i 56789sigma and triggered" %(a,b,c),[sigma_list,triggered5_list,triggered6_list,triggered7_list,triggered8_list,triggered9_list])

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

main_trigger(0,5,59,1e3,40e3)
































#    for k in date_list:
#        date_listshort.append(k[-16:-4])        
#    print (date_listshort)
#    for l in date_listshort:
#        year,month,day,hour,minute,second = l[-16:-14],l[-14:-12],l[-12:-10],l[-10:-8],l[-8:-6],l[-6:-4]
#        print day
 #   print (len(triggered_list))
  #  print (len(sigma_list))
   # print (triggered_list)
    #print (sigma_list)

#    for sigma_value in sigma_list[:-1]:                                                               #Een lijst maken met de sigmavalues, evenvaak als de samples
#        sigma2_list.extend([5*sigma_value]*(samples_per_sigma)) 
#    sigma2_list.extend([5*sigma_list[-1]]*(rest_len))
     
#    np.savetxt("30050218_45_3.txt",(triggered_list,sigma_list))
 
    #time = np.arange(1,2*c*(b-a),2)
    #time= pd.date_range("29/01/2018 09:00:002",periods = (b-a), freq = "119 min 59 S")
 

#    time_list2 = []
#    for j in dateandtime_list:
#        time_list2.extend([j]*59)