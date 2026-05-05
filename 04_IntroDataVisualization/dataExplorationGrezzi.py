import numpy as np
import pandas as pd
import scipy.optimize as opt
import matplotlib.pyplot as plt
import sys

rawDataFile = "Grezzi.xls"
# Proviamo a caricare i dati e vedere cosa contiene il df
datiRaw = pd.read_excel(rawDataFile)
print(datiRaw)


# Sistemiamo l'importazione del dataframe
datiRaw = pd.read_excel(rawDataFile, header=1)
print(datiRaw)


# Esploriamo il contenuto

print(f".describe\n{datiRaw.describe()}")
print(f".info\n{datiRaw.info()}")
print(datiRaw.columns)

lColonne = ["time", "OD", "Glc", "etoh", "Glu", "AKG", "Gly", "Fum"]


# Possiamo provare a caricare tutti i figli di excel `sheet_name=None`
datiRaw = pd.read_excel(rawDataFile, header=1, sheet_name=None)
print(datiRaw)
print(type(datiRaw))


# Si ottiene un dizionario di dataframe
dDatiRaw = pd.read_excel(rawDataFile, header=1, sheet_name=None)
for dfName in dDatiRaw:
    print(dfName)
    print(dDatiRaw[dfName])


# Si possono fondere i dataframe in un unico dataframe
dfDati = pd.concat(dDatiRaw)
print(dfDati)


# Si possono anche concatenare evitando che venga costruito un indice multi-level
dfDati = pd.concat(dDatiRaw, ignore_index=True)
print(dfDati)


# così si perde informazione. Si può decidere di mantere la stessa informazione (sheet_name) in una colonna
for dfName in dDatiRaw:
    dDatiRaw[dfName]["exp"] = dfName
    print(dDatiRaw[dfName])
dfDati = pd.concat(dDatiRaw, ignore_index=True)
print(dfDati)


# --------------------
# Restringiamo dati a solo quelli di interesse
dfOD = dfDati[["exp", "time", "OD"]].copy()
print(dfOD)


# individuiamo in NaN
print(dfOD.info())

# Eliminiamo righe che hanno NaNs
dfOD.dropna(subset="OD", inplace=True)
print(dfOD.info())

# Possiamo ricostruire l'informazione sulla fonte dati?
# Vediamo cosa ci dice il nome dell'esperimento. Ha una struttura?

print("Unique -----\n", dfOD.exp.unique())
# La struttura è EXPTag+Fonte+Progressivo i.e. AGlut2: exp A, fonte Glutammato, secondo esperimento
# Possiamo estrarre fonte?
dfOD["fonteTmp"] = dfOD.exp.str[1:-1]
print(dfOD.sample(10))
#         exp  time      OD fonte
# 287   JAmm2  22.0   3.950   Amm
# 48    CGlut   1.5   0.235   Glu
# 235   IAmm1  55.0   5.030   Amm
# 25    BGlut  32.0   2.440   Glu
# 113  EGlut2  21.5   0.193  Glut
# 219   HAmm2   4.5   0.970   Amm
# 250   IAmm2  72.0   5.360   Amm
# 149    FAmm   4.5   1.200    Am
# 143   FGlut  31.0  21.800   Glu
# 222   HAmm2  24.0   6.900   Amm

# Con regular expressions [regex101: build, test, and debug regex](https://regex101.com/) :
dfOD["fonte"] = dfOD.exp.str.extract(r"^[A-Z]([A-Za-z]+)\d*")
print(dfOD.sample(10))
dfOD.drop(columns=["fonteTmp"], inplace=True)
print(dfOD.sample(10))

# Ora Possiamo separare gli esperimenti in base alla fonte nutrititva
dfODAmm = dfOD[dfOD.fonte == "Amm"]
dfODGlut = dfOD[dfOD.fonte == "Glut"]

# Controlliano le dimensioni per verificare di non aver perso osservazioni:
print(f"{dfOD.shape[0]} nRecordOD ")
print(
    f"{dfODAmm.shape[0] + dfODGlut.shape[0]} = {dfODAmm.shape[0]} nRecordAmm + {dfODGlut.shape[0]} nRecordGlut"
)


figOD = plt.figure(figsize=(10, 10))
plt.xlabel("time [h]")
plt.ylabel("OD")
plt.grid()
plt.title("crescita su tutte le fonti")
plt.plot(dfOD.time, dfOD.OD, "o")
plt.show()

figODAmm = plt.figure(figsize=(10, 10))
plt.xlabel("time [h]")
plt.ylabel("OD")
plt.grid()
plt.title("crescita su Ammonio")
plt.plot(dfODAmm.time, dfODAmm.OD, "o")
plt.show()

figODGlut = plt.figure(figsize=(10, 10))
plt.xlabel("time [h]")
plt.ylabel("OD")
plt.grid()
plt.title("crescita su Glutammato")
plt.plot(dfODGlut.time, dfODGlut.OD, "o")
plt.show()


# it is possible to describe a population growth by means of the sigmoid (logistic) function.
# We can leverage the definition of a python function to draw such a function:
# [Logistic function - Wikipedia](https://en.wikipedia.org/wiki/Logistic_function)
def sigmoid(xIn, yMax, xMidpoint, kSteep):
    return yMax / (1.0 + np.exp(-kSteep * (xIn - xMidpoint)))


xi = np.linspace(0, 150)
yi = sigmoid(xi, 10, 40, 0.2)

figODGlut = plt.figure(figsize=(10, 10))
plt.xlabel("time [h]")
plt.ylabel("sigmoid")
plt.grid()
plt.title("crescita su Glutammato")
plt.plot(xi, yi, "o")
plt.show()


# Per tentare di allineare le serie temporali, si potrebbe tentare di fittare ciascuna curva con una sigmoide e sfruttare il xMidPont per traslare i tempi di ciascuna curva

time = dfODAmm.loc[dfODAmm.exp == "HAmm1", "time"]
odExp = dfODAmm[dfODAmm.exp == "HAmm1"].OD

# [scipy.optimize.curve_fit — SciPy v1.10.1 Manual](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)
fitParams, fitCovariance = opt.curve_fit(
    sigmoid, time, odExp, p0=[25.0, 24.0, 0.25]
)
print(fitParams)
print(fitCovariance)

odFitted = sigmoid(time, fitParams[0], fitParams[1], fitParams[2])


figODHAmm1fit = plt.figure(figsize=(10, 10))
ax = figODHAmm1fit.add_subplot(111)
ax.set_xlabel("time [h]")
ax.set_ylabel("sigmoid")
ax.grid()
ax.set_title("crescita su Ammonio")
ax.plot(time, odExp, "o")
ax.plot(time, odFitted, "or")
plt.show()

