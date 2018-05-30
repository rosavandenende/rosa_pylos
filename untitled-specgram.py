#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 28 16:53:51 2018

@author: chip
"""

import matplotlib.pyplot as plt
import wave
import struct


def main(n):
    time_series = []
    waveFile = wave.open('/home/chip/Downloads/pylos20180411.wav','r')
    Fs = waveFile.getframerate()
    length = waveFile.getnframes()
    for i in range(0,int(n)):
        waveFile.setpos(i)
        
        waveData = waveFile.readframes(1)
        sample_point = struct.unpack('<h', waveData)
        time_series.append(sample_point[0])
        
    fig,(ax1,ax2) = plt.subplots(2,figsize=(24,16))
    plt.subplots_adjust(hspace = 0.5)
    ax1.plot(range(0,int(n)),time_series)
    ax1.set(title='Time series', xlabel = 'sample number',ylabel = 'ADC')
    values,ybins,xbins,im = ax2.specgram(time_series, Fs = Fs)
    ax2.set(title='Spectogram', xlabel = 'Time (seconds)',ylabel = 'Frequency (Hz)')
    cbar = fig.colorbar(im,ax=ax2)
    cbar.set_label('Intensity (dB)')
    

    
    plt.show()
    
    
    
main(2*1e7)


