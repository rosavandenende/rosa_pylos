#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:01:35 2018

@author: rosavandenende
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 16:51:05 2018

@author: rosavandenende
"""



#in dit document: plotten van de triggers en sigma, lange bestand

import matplotlib.pyplot as plt
#from datetime import datetime, timedelta,num2date
import matplotlib.dates as mdates
import pandas as pd 


daterange = pd.date_range("29/01/2018 09:00:02",periods = 2950, freq = "2min")

file = open("sigmatrig0_50_59",'r')
lines = file.readlines()
sigma = lines[0]
trigger = lines[1]
sigma_list = sigma.split()
trigger_list = trigger.split()


plt.rcParams["figure.figsize"] = [24,14]
fig, ax = plt.subplots(2,1,sharex = False)

ax[0].scatter(daterange,sigma_list,s=8)
ax[0].set_xlabel("Date (y-m-d h:min)")
ax[0].set_ylabel("Noise level, 5$\sigma$")
ax[0].set_xlim(pd.Timestamp("2018-01-29"),pd.Timestamp("2018-02-03"))
ax[0].set_xlim(pd.Timestamp("2018-01-29"),pd.Timestamp("2018-02-03"))
xfmt = mdates.DateFormatter("%d-%m-%y %H:%M")
ax[0].xaxis.set_major_formatter(xfmt)



ax[1].scatter(daterange,trigger_list,s=8)
ax[1].set_xlabel("Date (y-m-d h:min)")
ax[1].set_ylabel("Number of triggers")
ax[1].set_xlim(pd.Timestamp("2018-01-29"),pd.Timestamp("2018-02-03"))
ax[1].set_xlim(pd.Timestamp("2018-01-29"),pd.Timestamp("2018-02-03"))
xfmt = mdates.DateFormatter("%d-%m-%y %H:%M")
ax[1].xaxis.set_major_formatter(xfmt)

plt.show()
