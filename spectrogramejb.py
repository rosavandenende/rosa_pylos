#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 14:51:15 2018

@author: rosavandenende
"""

import wave, struct
from math import *
import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt
from scipy import signal
import sys
import pylab
import os
from scipy.signal import butter, lfilter
import datetime
import string

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

def get_timestamp(filename, begin_time):
    s = os.path.splitext(os.path.basename(filename))[0][10:]
    extra_minute = int(begin_time/60.)
    extra_second = int(begin_time - extra_minute*60.)

    hours = int(s[6:8])
    minutes = int(s[8:10]) + extra_minute
    seconds = int(s[10:12]) + extra_second
    if seconds > 60:
        minutes += 1
        seconds -= 60
    if minutes > 60:
        hours +=1
        minutes -= 60
        
    date = datetime.datetime(year=2000+ int(s[0:2]), month=int(s[2:4]), \
                             day=int(s[4:6]), \
                             hour = hours, minute = minutes, second = seconds)
    return date

def graph_spectrogram(wav_file, begin, end, cutoff_low, cutoff_high, order):
    sound_info, Fs = get_wav_info(wav_file)
    pylab.figure(num=None, figsize=(19, 12))
    pylab.subplot(111)
    pylab.title('spectrogram of %r' % wav_file)
    nfft = 1024
    data = sound_info[begin*Fs: end*Fs]
    data = butter_bandpass_filter(data, cutoff_low, cutoff_high, Fs, order)
    pylab.specgram(data, Fs=Fs, NFFT = nfft, \
                   noverlap =int(nfft/2), cmap='viridis_r', \
                   mode = 'psd')
    pylab.ylim(0,20000)
    pylab.colorbar()
    datestring = get_timestamp(wav_file, begin)
    pylab.xlabel("Time (seconds since {}) [s]".format(datestring), \
                 size = 16, ha ='right', x=1.0)
    pylab.ylabel("PSD", size = 16, ha ='right', position=(0,1))
    pylab.savefig('spectrogram.png')
    pylab.show()
    
def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate

def main(argv):
    begin = 0
    end = 100
    if len(argv) > 1:
        filename  = argv[1]
    if len(argv) > 2:
        begin = string.atoi(argv[2]) # in seconds
        end = string.atoi(argv[3]) # seconds

    filename = argv[1]
    cutoff_low = 5000
    cutoff_high = 70000
    order = 5 
    graph_spectrogram(filename, begin, end, cutoff_low, cutoff_high, order)


#argv = "201650198.180220085641.wav", 1, 5

graph_spectrogram("201650198.180220085641.wav",4440,4450,1000,70000,5)
