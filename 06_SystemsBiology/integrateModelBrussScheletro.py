import numpy as np
import matplotlib.pyplot as plt
# from scipy.integrate import odeint
import scipy.integrate as spi


A = 1.0
B = 3.0
k1 = 1.0
k2 = 1.0
k3 = 1.0
k4 = 1.0


def myCauchy(y, t):

    return [dy0, dy1]

time = np.linspace(0.0, 20.0, 1000)
yInit = np.array([1.0, 1.0])
y = spi.odeint(myCauchy, yInit, time)

plt.style.use(['lezioneBlack'])
plt.grid()
plt.xlabel('t', fontsize=22)
plt.ylabel('y(t)', fontsize=22)
plt.plot(time, y[:, 0], '-', label='X', color='#377EB8')
plt.plot(time, y[:, 1], '-', label='Y', color='#E41A1C')
plt.legend()
fileName = 'brussODEpy.pdf'
plt.savefig(fileName, format='pdf')
plt.show()
