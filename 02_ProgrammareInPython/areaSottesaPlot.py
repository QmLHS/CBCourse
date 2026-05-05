import matplotlib.pyplot as plt


def effe(x):
    y = -x * (x - 1.0)
    return y


numIntervalli = input('inserire il numero di intervalli in [0.0, 1.0] ')

deltaIntervallo = 1.0 / float(numIntervalli)
print("larghezza intervallo", deltaIntervallo)

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

print("l'area sottesa dalla curva vale ", areaSottesa)

plt.bar(xIntervalli, yIntervalli, width=deltaIntervallo, color='b', alpha=0.56)
plt.plot(xIntervalli, yIntervalli, 'ro-')
plt.show()
