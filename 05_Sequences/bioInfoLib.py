#!/usr/bin/env ipython
# -*- coding: utf-8 -*-
import Bio.SeqIO as seqIO
import numpy as np

COLORDICT = {
    'red': '#E41A1C',
    'blue': '#377EB8',
    'green': '#4DAF4A',
    'purple': '#984EA3',
    'orange': '#FF7F00',
    'yellow': '#FFFF33',
    'brown': '#A65628',
    'lgrey': '#C0C0C0',
    'lgrey2': '#808080',
    'black': '#000000'
}

BASECOLORS = {
    'A': 'green',
    'C': 'blue',
    'G': 'black',
    'T': 'red'
}


def ab1ToAscii(fileName):
    fileStream = open(fileName, 'rb')
    fileContent = []
    # print '-------------'
    for record in seqIO.parse(fileStream, "abi"):
        # print record
        fileContent.append(record)
    # print '-------------'
    fileStream.close()
    return fileContent


def ab1ToRecord(fileName):
    fileStream = open(fileName, 'rb')
    record = seqIO.read(fileStream, "abi")
    return record


def ab1Data2DATAX(fileName, dataChannelName):
    with open(fileName, 'r') as fileStream:
        data = fileStream.read()
        fileStream.close()
    strStart = data.find(dataChannelName)
    strStart += len(dataChannelName + ": (") + 1
    # print data[strStart: strStart +50]
    strEnd = data[strStart:].find("),")
    # print data[strStart: strStart+ strEnd]
    data = np.array(data[strStart: strStart + strEnd].split(','), dtype=float)
    return data


def ab1Data2STR(fileName, dataChannelName):
    with open(fileName, 'r') as fileStream:
        data = fileStream.read()
        fileStream.close()
    strStart = data.find(dataChannelName)
    strStart += len(dataChannelName + ": '") + 1
    # print data[strStart: strStart +50]
    strEnd = data[strStart:].find("',")
    # print data[strStart: strStart+ strEnd]
    data = np.array(list(data[strStart: strStart + strEnd]), dtype='|S1')
    return data
