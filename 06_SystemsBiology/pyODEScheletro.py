# to use this script:
# iPython pyODE.py modelFileName Volume tEnd

import modelParser as mP
import numpy as np
import scipy.integrate as spi
import sys
import matplotlib.pyplot as plt


fileModelName = sys.argv[1]
print(fileModelName)
Vol = float(sys.argv[2])
tEnd = float(sys.argv[3])

iRulesLines, iSpecsLines, iFeedsLines = mP.findRulesAndSpecs(fileModelName)
aRules, aConstants = mP.rulesAndConstants(fileModelName, iRulesLines)
dictAlphabet = mP.rulesToAlphabet(aRules)
print("alphabet:index \t\t", dictAlphabet)
leftSide, rightSide, delta = mP.rulesToMatrices(aRules, dictAlphabet)
leftSide = leftSide.astype(float)
rightSide = rightSide.astype(float)
delta = delta.astype(float)
print("L\n", leftSide, "\n")
print("R\n", rightSide, "\n")
print("D\n", delta, "\n")
aConstants = aConstants.astype(float)
print("c ", aConstants)

X = mP.speciesInit(fileModelName, iSpecsLines, dictAlphabet).astype(float)
print("X_in: ", X)
dictFeedSpecs = mP.speciesInFeed(fileModelName, iFeedsLines, dictAlphabet, X)
print("dictFeed:\n", dictFeedSpecs)

approachIn = mP.modellingApproach(fileModelName)
if 'Stoc' in approachIn:
    print("Stoch->Det")
    X, aConstants = mP.stoch2Det(Vol, X, leftSide, aConstants)
print("X: ", X)
print("K: ", aConstants)


def myCauchy(x, t):
    return dx


print("\n")


time = np.linspace(0.0, tEnd, 10000)
yInit = X
y = spi.odeint(myCauchy, yInit, time, atol=1e-9)

print(y[-1] * Vol * 6.022e23)
plt.grid()
plt.xlabel('t', fontsize=22)
plt.ylabel('y(t)', fontsize=22)
for spec in dictAlphabet:
    plt.plot(time, y[:, dictAlphabet[spec]] * Vol * 6.022e23, '-', label=spec)
plt.legend()
fileName = fileModelName + 'ODEpy.pdf'
plt.savefig(fileName, format='pdf')
plt.show()
