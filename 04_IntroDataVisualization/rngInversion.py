import numpy as np
import matplotlib.pyplot as plt


def effe(tau, a0):
    return a0 * np.exp(-a0 * tau)


def invEffe(r, a0):
    return (1.0 / a0) * np.log(1.0 / r)


rngs = np.random.rand(200)
invF = invEffe(rngs, 0.5)
xs = np.linspace(0, invF.max(), 50)

hist, bins = np.histogram(rngs, bins=10, normed=1)
# hist = hist / float(hist.max())
width = 0.9 * (bins[1] - bins[0])
center = .5 * (bins[:-1] + bins[1:])


# plt.style.use(['informalBlack'])
# plt.rc('text', usetex=True)
fig = plt.figure(figsize=(10, 10))
plt.grid()
plt.xlabel('rng')
plt.ylabel('inv(F)')
plt.bar(center, hist, align='center', width=width,
        alpha=0.5, color='#4DAF4A',
        label='freq(r)')
plt.plot(rngs, invEffe(rngs, 0.5), '.',
        color='#377EB8',
        label='generated Tau')
# plt.plot(t, y, 'o', label='Runge Khutta approx')
plt.legend()
fileName = 'rngInvEffe.pdf'
plt.savefig(fileName, format='pdf',
            orientation='landscape',
            transparent=True)
plt.close(fig)


hist, bins = np.histogram(invEffe(rngs, 0.5), bins=10, normed=1)
# hist = hist / float(hist.max())
width = 0.9 * (bins[1] - bins[0])
center = .5 * (bins[:-1] + bins[1:])
fig = plt.figure(figsize=(10, 10))
plt.xlabel('tau')
plt.ylabel('freq(tau)')
plt.plot(xs, effe(xs, 0.5), '-',
        color='#E41A1C', label='Taus Analitical Distrib')
plt.bar(center, hist, align='center', width=width,
        color='#377EB8', alpha=0.5,
        label='Sampled Taus')
# plt.plot(t, y, 'o', label='Runge Khutta approx')
plt.legend()
fileName = 'rngInv.pdf'
plt.savefig(fileName, format='pdf',
            orientation='landscape',
            transparent=True)
plt.close(fig)
# plt.show()
