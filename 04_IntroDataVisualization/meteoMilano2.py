import numpy as np
import matplotlib.pyplot as plt

fileName = 'MeteoMilano.csv'

fileDati = open(fileName, 'r')
fileLines = fileDati.readlines()
fileDati.close()

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

numRighe = len(fileLines)

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

# 2015-3-19
datiMarzo = matriceDataTemp[:, 1] == 3
# print datiMarzo
matriceMarzo = matriceDataTemp[datiMarzo]
# print matriceMarzo

mediaMarzo = np.mean(matriceMarzo[:, 3])
print (mediaMarzo)
# plt.plot([np.min(matriceMarzo[:, 2]), np.max(matriceMarzo[:, 2])],
#          [mediaMarzo, mediaMarzo])
# plt.plot(matriceMarzo[:, 2], matriceMarzo[:, 3], 'ro')
# plt.show()


# matriceMarzo2011 = matriceMarzo[matriceMarzo[:, 0] == 2011]
# matriceMarzo2012 = matriceMarzo[matriceMarzo[:, 0] == 2012]
# matriceMarzo2013 = matriceMarzo[matriceMarzo[:, 0] == 2013]
# print matriceMarzo2011

# plt.plot(matriceMarzo[:, 2], matriceMarzo[:, 3], 'ro')
# plt.plot(matriceMarzo2011[:, 2], matriceMarzo2011[:, 3], 'r-')
# plt.plot(matriceMarzo2012[:, 2], matriceMarzo2012[:, 3], 'g-')
# plt.plot(matriceMarzo2013[:, 2], matriceMarzo2013[:, 3], 'b-')
# plt.show()

# m2011 = matriceDataTemp[matriceDataTemp[:, 0] == 2011.0]
# print m2011
# m2011Mese = m2011[m2011[:, 1] == 6]
# print m2011Mese

primoAnno = int(np.min(matriceDataTemp[:, 0]))
ultimoAnno = int(np.max(matriceDataTemp[:, 0]))
numeroAnni = (ultimoAnno - primoAnno) + 1
mediaMeseAnno = np.empty((int(numeroAnni) * 12, 3))
# print range(primoAnno, ultimoAnno)

# for anno in range(primoAnno, ultimoAnno):
#     matriceAnno = matriceDataTemp[matriceDataTemp[:, 0] == anno]
#     print matriceAnno.shape
contatore = 0
for anno in range(primoAnno, ultimoAnno + 1):
    matriceAnno = matriceDataTemp[matriceDataTemp[:, 0] == anno]
    # print matriceAnno
    for mese in range(1, 12 + 1):
        matriceMeseAnno = matriceAnno[matriceAnno[:, 1] == mese]
        # print matriceMeseAnno
        mediaMeseAnno[contatore, 0] = anno
        mediaMeseAnno[contatore, 1] = mese
        # mediaMeseAnno[contatore, 2] = np.mean(matriceMeseAnno[:,3])
        if matriceMeseAnno.size > 0:
            mediaMeseAnno[contatore, 2] = np.mean(matriceMeseAnno[:, 3])
        contatore += 1

# print mediaMeseAnno
# plt.plot(np.arange(len(mediaMeseAnno)), mediaMeseAnno[:, 2], 'b-')
# print mediaMeseAnno[:, 0] == 2011
# print mediaMeseAnno[mediaMeseAnno[:, 0] == 2011]

plt.grid()
plt.xlabel('mese')
plt.ylabel('< t >  [gradi C]')
for anno in range(primoAnno, ultimoAnno + 1):
    indiciAnno = mediaMeseAnno[:, 0] == anno
    plt.plot(mediaMeseAnno[indiciAnno, 1], mediaMeseAnno[indiciAnno, 2], 'o-')
plt.show()
