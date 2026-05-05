#!/usr/bin/env ipython
# -*- coding: utf-8 -*-
import sys
import numpy as np
from scipy import signal as sig
import matplotlib.pyplot as plt
import bioInfoLib as bil


filename = sys.argv[1]
# data load
print('channels order', bil.ab1Data2STR(filename, 'FWO_1'))
# G black/yellow
# A green
# C blue
# T red
# FWO_1 = 'GATC' <-> 9,10,11,12
dataG = bil.ab1Data2DATAX(filename, 'DATA9')


# peak Detection
peakWidth = 10
peaksG = sig.find_peaks_cwt(dataG, np.arange(1, peakWidth))


# verify peaks location
baseMax = 1000
figSeq = plt.figure(figsize=(15, 9))
ax = figSeq.add_axes([0.1, 0.05, 0.85, 0.9])
plt.xlim(0, baseMax)
plt.plot(dataG[:baseMax:], c='k', alpha=0.7)
plt.plot(peaksG[:baseMax], peaksG[:baseMax], 500,
         marker='o', linestyle='None',
         c='k')
plt.savefig('electropherogramPeaks.pdf',
            format='pdf',
            orientation='landscape',
            transparent=True)
plt.close()



# base calls
# baseCalledFromPeaks = ...


# compare sequences
# 'PLOC2' Array of peak locations as called by Basecaller
# peaksLocation = np.array(data)

# 'PBAS2' Array of sequence characters as called by Basecaller
# sangerCalledBases = data 'PBAS2'

# print(sangerCalledBases == baseCalledFromPeaks)
