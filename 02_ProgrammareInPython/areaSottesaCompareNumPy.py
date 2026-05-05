import numpy as np
import timeit


def effe(x):
    y = -x * (x - 1.0)
    return y


numIntervalli = input('inserire il numero di intervalli in [0.0, 1.0] ')

deltaIntervallo = 1.0 / float(numIntervalli)
print("larghezza intervallo", deltaIntervallo)

start = timeit.default_timer()
xIntervalli = []
yIntervalli = []
i = 0
while i < numIntervalli:
    xIntervallo = i * deltaIntervallo
    xIntervalli.append(xIntervallo)
    yIntervalli.append(effe(xIntervallo))
    i += 1

areaSottesa = 0.0
for altezza in yIntervalli:
    areaSottesa += altezza * deltaIntervallo
endOld = timeit.default_timer()
print("l'area sottesa dalla curva vale ", areaSottesa)

xNPIntervalli = np.linspace(0.0, 1.0, numIntervalli, endpoint=False)
yNPIntervalli = -xNPIntervalli * (xNPIntervalli - 1.0)
npArea = np.sum(yNPIntervalli * deltaIntervallo)
endNP = timeit.default_timer()
# print( xNPIntervalli)
# print( xIntervalli)
# print( yNPIntervalli)
# print( yIntervalli)
print("area numpy = ", npArea)

print("old timing = ", endOld - start, "numPy timing = ", endNP - endOld)
