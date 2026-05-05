# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt


T0 = 0.0
TF = 10.0
STEPS = 10
Y0 = 100.0
K = 0.5


def effe(x):

    return y


t = np.linspace(T0, TF, STEPS + 1, dtype=float, endpoint=True)
y = np.empty(STEPS + 1, dtype=float)
h = (TF - T0) / STEPS

print(h, t[1] - t[0])

y[0] = Y0
i = 1
while i <= STEPS:

    i += 1

print t
print y

analitica = Y0 * np.exp(- K * t)


plt.grid()
plt.xlabel('t')
plt.ylabel('y(t)')
plt.plot(t, analitica, '-', label='Analitical solution')
plt.plot(t, y, 'o', label='Runge Khutta approx')
plt.legend()
fileName = 'rk' + str(STEPS) + '.pdf'
plt.savefig(fileName, format='pdf')
plt.show()
