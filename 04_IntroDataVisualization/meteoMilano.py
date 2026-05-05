import numpy as np
import matplotlib.pyplot as plt

fileName = 'MeteoMilano.csv'

fileDati = open(fileName, 'r')
# fileCompleto = fileDati.read()
# print fileCompleto
# print type(fileCompleto)

# una riga per volta
# linea = fileDati.readline()
# print linea
# linea = fileDati.readline()
# print linea

# for linea in fileDati:
#     print linea
# fileDati.close()

fileLines = fileDati.readlines()
fileDati.close()

print (type(fileLines))
print (type(fileLines[2]))

intestazione = fileLines[0]
del fileLines[0]
# [0]  CET
#      Temperatura maxC
#      Temperatura mediaC
#      Temperatura minC
#      Punto di rugiadaC
#      MeanDew PointC
#      Min DewpointC
#      Max Umidità
#      Mean Umidità
# [9]  Min Umidità
#      Max Pressione a livello del marehPa
#      Mean Pressione a livello del marehPa
#      Min Pressione a livello del marehPa
#      Max VisibilitàKm
#      Mean VisibilitàKm
#      Min VisibilitàkM
#      Max Velocità del ventoKm/h
#      Mean Velocità del ventoKm/h
#      Max Velocità RafficaKm/h
# [19] Precipitazionimm
#      CloudCover
#      Eventi
#      WindDirDegrees

print (fileLines[0])
numRighe = len(fileLines)

# riga = fileLines[0].strip('\n')  # elimina \n
# tokens = riga.split(',')
tokens = fileLines[0].strip('\n').split(',')  # spezza in parole la riga
print ("---",tokens)

i = 0
tempMean = np.empty(numRighe, float)
for line in fileLines:
    tokens = line.strip('\n').split(',')
    if tokens[2] != '':
        tempMean[i] = float(tokens[2])
    i += 1

print (tempMean)
print(tempMean.mean())




plt.plot(np.arange(numRighe), tempMean, 'ro-')
plt.show()

i = 0
matriceDataTemp = np.empty((numRighe, 4), float)
for line in fileLines:
    tokens = line.strip('\n').split(',')
    if tokens[0] != '':
        datiData = tokens[0].split('-')
        matriceDataTemp[i, 0] = datiData[0]
        matriceDataTemp[i, 1] = datiData[1]
        matriceDataTemp[i, 2] = datiData[2]
    if tokens[2] != '':
        matriceDataTemp[i, 3] = float(tokens[2])
    i += 1
# print matriceDataTemp


plt.plot(np.arange(numRighe), matriceDataTemp[:, 3])
plt.show()
