#!/usr/bin/env ipython
# -*- coding: utf-8 -*-
# import os
import sys
import numpy as np
from scipy import signal as sig
# import glob
# import pandas as pd
import matplotlib.pyplot as plt
import bioInfoLib as bil

filename = sys.argv[1]

print('channels order', bil.ab1Data2STR(filename, 'FWO_1'))
# G black/yellow
# A green
# C blue
# T red
# FWO_1 = 'GATC' <-> 9,10,11,12
dataG = bil.ab1Data2DATAX(filename, 'DATA9')
dataA = bil.ab1Data2DATAX(filename, 'DATA10')
dataT = bil.ab1Data2DATAX(filename, 'DATA11')
dataC = bil.ab1Data2DATAX(filename, 'DATA12')
print(dataG.dtype)

peakWidth = 10
peaksG = sig.find_peaks_cwt(dataG, np.arange(1, peakWidth))
print(peaksG.shape)
print(peaksG)
peaksA = sig.find_peaks_cwt(dataA, np.arange(1, peakWidth))
print(peaksA.shape)
print(peaksA)
peaksT = sig.find_peaks_cwt(dataT, np.arange(1, peakWidth))
print(peaksT.shape)
print(peaksT)
peaksC = sig.find_peaks_cwt(dataC, np.arange(1, peakWidth))
print(peaksC.shape)
print(peaksC)


baseMax = 1000
figSeq = plt.figure(figsize=(15, 9))
ax = figSeq.add_axes([0.1, 0.05, 0.85, 0.9])
plt.xlim(0, baseMax)
plt.plot(dataG[:baseMax:], c='k', alpha=0.7, marker='o')
plt.plot(peaksG[:baseMax], np.full(peaksG[:baseMax].size, 500),
         marker='o', linestyle='None',
         c='red')
         # c=bil.COLORDICT[bil.BASECOLORS['G']])
plt.savefig('electropherogramPeaks.pdf',
            format='pdf',
            orientation='landscape',
            transparent=True)
plt.close()

# 'PLOC2' Array of peak locations as called by Basecaller
# peaksLocation = np.array(data.annotations['abif_raw']['PLOC2'])
peaksLocation = bil.ab1Data2DATAX(filename, 'PLOC2')
print('peaks location ', peaksLocation.shape)
print(peaksLocation)
# 'PBAS2' Array of sequence characters as called by Basecaller
baseCalls = bil.ab1Data2STR(filename, 'PBAS2')
print('called bases ', len(baseCalls), baseCalls.dtype)
print("baseCalls:\n", baseCalls)

basesToShow = peaksLocation[peaksLocation <= baseMax]
print('location of last base ', basesToShow[-1])
idxBaseToShow = basesToShow[:-1].shape[0]
print('idx last base to show: ', idxBaseToShow)

figSeq = plt.figure(figsize=(15, 9))
ax = figSeq.add_axes([0.1, 0.05, 0.85, 0.9])
plt.xlim(0, baseMax)
plt.plot(dataG[:baseMax:], c=bil.COLORDICT[bil.BASECOLORS['G']], alpha=0.7)
plt.plot(dataA[:baseMax:], c=bil.COLORDICT[bil.BASECOLORS['A']], alpha=0.7)
plt.plot(dataC[:baseMax:], c=bil.COLORDICT[bil.BASECOLORS['C']], alpha=0.7)
plt.plot(dataT[:baseMax:], c=bil.COLORDICT[bil.BASECOLORS['T']], alpha=0.7)
plt.plot(peaksG[:baseMax], np.full(peaksG[:baseMax].size, 1950.0),
         marker='o', linestyle='None',
         c=bil.COLORDICT[bil.BASECOLORS['G']])
plt.plot(peaksA[:baseMax], np.full(peaksA[:baseMax].size, 1950.0),
         marker='o', linestyle='None',
         c=bil.COLORDICT[bil.BASECOLORS['A']])
plt.plot(peaksT[:baseMax], np.full(peaksT[:baseMax].size, 1950.0),
         marker='o', linestyle='None',
         c=bil.COLORDICT[bil.BASECOLORS['T']])
plt.plot(peaksC[:baseMax], np.full(peaksC[:baseMax].size, 1950.0),
         marker='o', linestyle='None',
         c=bil.COLORDICT[bil.BASECOLORS['C']])
for i, base in enumerate(baseCalls[:idxBaseToShow]):
    strBase = base.decode()  # requested to adapt to python 3
    ax.text(peaksLocation[i], 2000.0,
            strBase, fontsize=12, color=bil.COLORDICT[bil.BASECOLORS[strBase]])
plt.savefig('chromatographyPeaks.pdf',
            format='pdf',
            orientation='landscape',
            transparent=True)
plt.close()


baseCalledFromPeaks = np.full(baseMax, 'X', dtype='|S1')
print(baseCalledFromPeaks.shape, baseCalledFromPeaks.dtype)
baseCalledFromPeaks[peaksG[peaksG < baseMax]] = 'G'
baseCalledFromPeaks[peaksA[peaksA < baseMax]] = 'A'
baseCalledFromPeaks[peaksT[peaksT < baseMax]] = 'T'
baseCalledFromPeaks[peaksC[peaksC < baseMax]] = 'C'
baseCalledFromPeaks = baseCalledFromPeaks[baseCalledFromPeaks != b'X'].copy()
print('----\n', baseCalledFromPeaks, '\n----\n')


sangerCalledBases = np.full(len(basesToShow) - 1, 'X', dtype='|S1')
for i, el in enumerate(baseCalls[:idxBaseToShow]):
    sangerCalledBases[i] = el
print(sangerCalledBases)

for i in range(len(sangerCalledBases)):
    print(sangerCalledBases[i], baseCalledFromPeaks[i],
          sangerCalledBases[i] == baseCalledFromPeaks[i])
