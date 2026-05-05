# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

A = 2.0
samples = 100

x = np.linspace(0, 10, samples)
Px = A * np.exp(-A * x)
Fx = 1.0 - np.exp(-A * x)

print(Fx[-1])


plt.grid()
plt.plot(x, Px, 'ro')
plt.plot(x, Fx, 'b-')
plt.show()
