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
deltaT = (TF - T0) / STEPS

print deltaT, t[1] - t[0]

y[0] = Y0
i = 1
while i <= STEPS:

    i += 1

analitica = Y0 * np.exp(- K * t)

plt.style.use(['lezioneBlack'])
plt.grid()
plt.xlabel('t', fontsize=22)
plt.ylabel('y(t)', fontsize=22)
plt.plot(t, analitica, 'b-', label='analitical solution')
plt.plot(t, y, 'ro', label='euler approx')
plt.legend()
fileName = 'euler' + str(STEPS) + '.pdf'
plt.savefig(fileName, format='pdf')
plt.show()
