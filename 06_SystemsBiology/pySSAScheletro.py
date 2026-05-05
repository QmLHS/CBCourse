import modelParser as mP
import numpy as np

# da console cd "E:\percorso\percorso\"


def binCoeff(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in xrange(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0


def propensities(props, xIn, cIn, leftSideIn):


def tossTau(aZero):

    return tau


def tossRule(propensities, aZero):

    return mu


def applyRule(deltaMatrix, iRule, aX):


def feedStep(aX, dictFeed):



# caricamento modello tramite libreria
fileModelName = "model"
iRulesLines, iSpecsLines, iFeedsLines = mP.findRulesAndSpecs(fileModelName)
aRules, aConstants = mP.rulesAndConstants(fileModelName, iRulesLines)
dictAlphabet = mP.rulesToAlphabet(aRules)
print("alphabet:index \t\t", dictAlphabet)
leftSide, rightSide, delta = mP.rulesToMatrices(aRules, dictAlphabet)
print(leftSide)
print(rightSide)
print(delta)

# apertura file per scrittura dati dynamica
fileName = "dynamics"
dynFile = open(fileName, 'a')

# caricamento condizioni iniziali e specie in feed
X = mP.speciesInit(fileModelName, iSpecsLines, dictAlphabet).astype(int)
dictFeedSpecs = mP.speciesInFeed(fileModelName, iFeedsLines, dictAlphabet, X)
print("dictFeed:\n", dictFeedSpecs)

# simulazione della dinamica
aPropensities = np.zeros(len(aRules), dtype=float)
t = 0.0
while (t < 50.0):
    propensities(aPropensities, X, aConstants, leftSide)
    # print aPropensities
    a0 = aPropensities.sum()
    deltaT = tossTau(a0)
    rule = tossRule(aPropensities, a0)
    # print deltaT, rule
    t += deltaT
    applyRule(delta, rule, X)
    feedStep(X, dictFeedSpecs)
    # print t, X
    dynFile.write(str(t) + '\t')
    # np.savetxt(dynFile, X, newline='\t')
    X.tofile(dynFile, sep="\t")
    dynFile.write('\n')

dynFile.close()
