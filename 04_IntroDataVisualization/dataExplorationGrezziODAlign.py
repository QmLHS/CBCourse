import numpy as np
import pandas as pd
import scipy.optimize as opt
import matplotlib.pyplot as plt
import sys

rawDataFile = "Grezzi.xls"
lColonne = ["time", "OD", "Glc", "etoh", "Glu", "AKG", "Gly", "Fum"]

# Si ottiene un dizionario di dataframe
dDatiRaw = pd.read_excel(rawDataFile, header=1, sheet_name=None)
for dfName in dDatiRaw:
    print(dfName)
    print(dDatiRaw[dfName])

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

# Con regular expressions [regex101: build, test, and debug regex](https://regex101.com/) :
dfOD["fonte"] = dfOD.exp.str.extract(r"^[A-Z]([A-Za-z]+)\d*")
print(dfOD.sample(10))

# Ora Possiamo separare gli esperimenti in base alla fonte nutrititva
dfODAmm = dfOD[dfOD.fonte == "Amm"]
dfODGlut = dfOD[dfOD.fonte == "Glut"]

# Controlliano le dimensioni per verificare di non aver perso osservazioni:
print(f"{dfOD.shape[0]} nRecordOD ")
print(
    f"{dfODAmm.shape[0] + dfODGlut.shape[0]} = {dfODAmm.shape[0]} nRecordAmm + {dfODGlut.shape[0]} nRecordGlut"
)


# figOD = plt.figure(figsize=(10, 10))
# plt.xlabel("time [h]")
# plt.ylabel("OD")
# plt.grid()
# plt.title("crescita su tutte le fonti")
# plt.plot(dfOD.time, dfOD.OD, "o")
# plt.show()

# figODAmm = plt.figure(figsize=(10, 10))
# plt.xlabel("time [h]")
# plt.ylabel("OD")
# plt.grid()
# plt.title("crescita su Ammonio")
# plt.plot(dfODAmm.time, dfODAmm.OD, "o")
# plt.show()

# figODGlut = plt.figure(figsize=(10, 10))
# plt.xlabel("time [h]")
# plt.ylabel("OD")
# plt.grid()
# plt.title("crescita su Glutammato")
# plt.plot(dfODGlut.time, dfODGlut.OD, "o")
# plt.show()


# it is possible to describe a population growth by means of the sigmoid (logistic) function.
# We can leverage the definition of a python function to draw such a function:
# [Logistic function - Wikipedia](https://en.wikipedia.org/wiki/Logistic_function)
def sigmoid(xIn, yMax, xMidpoint, kSteep):
    return yMax / (1.0 + np.exp(-kSteep * (xIn - xMidpoint)))


# Per tentare di allineare le serie temporali, si potrebbe tentare di fittare ciascuna curva con una sigmoide e sfruttare il xMidPont per traslare i tempi di ciascuna curva
time = dfODAmm.loc[dfODAmm.exp == "HAmm1", "time"]
odExp = dfODAmm[dfODAmm.exp == "HAmm1"].OD

# [scipy.optimize.curve_fit — SciPy v1.10.1 Manual](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)
fitParams, fitCovariance = opt.curve_fit(sigmoid, time, odExp, p0=[25.0, 24.0, 0.25])
print(fitParams)
print(fitCovariance)

odFitted = sigmoid(time, fitParams[0], fitParams[1], fitParams[2])


# figODHAmm1fit = plt.figure(figsize=(10, 10))
# ax = figODHAmm1fit.add_subplot(111)
# ax.set_xlabel("time [h]")
# ax.set_ylabel("sigmoid")
# ax.grid()
# ax.set_title("crescita su Ammonio")
# ax.plot(time, odExp, "o")
# ax.plot(time, odFitted, "or")
# plt.show()

lAmmExperiments = list(dfODAmm.exp.unique())
dfODAmm["yMax"] = -1.0
dfODAmm["xMid"] = -1.0
dfODAmm["kStp"] = -1.0
for exp in lAmmExperiments:
    time = dfODAmm.loc[dfODAmm.exp == exp, "time"]
    odExp = dfODAmm.loc[dfODAmm.exp == exp, "OD"]
    expFitParams, expFitCov = opt.curve_fit(
        sigmoid, time, odExp, p0=[25.0, 24.0, 0.25]
    )
    print(f"{exp} {expFitParams}")
    dfODAmm.loc[dfODAmm.exp == exp, "yMax"] = expFitParams[0]
    dfODAmm.loc[dfODAmm.exp == exp, "xMid"] = expFitParams[1]
    dfODAmm.loc[dfODAmm.exp == exp, "kStp"] = expFitParams[2]

print(dfODAmm)
xMidMin = dfODAmm.xMid.min()
xMidMax = dfODAmm.xMid.max()
print(xMidMin)

dfODAmm["timeShifted"] = dfODAmm.time - (dfODAmm.xMid - xMidMin) + xMidMax
print(dfODAmm)

figODHAmm1fit = plt.figure(figsize=(10, 10))
ax = figODHAmm1fit.add_subplot(111)
ax.set_xlabel("time [h]")
ax.set_ylabel("sigmoid")
ax.grid()
ax.set_title("crescita su Ammonio")
ax.plot(dfODAmm.timeShifted, dfODAmm.OD, "o")
plt.show()
