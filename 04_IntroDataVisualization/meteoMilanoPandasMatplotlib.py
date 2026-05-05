import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime


# dfMeteoMilano =\
    # pd.read_csv('MeteoMilano.csv',
                # converters={0: lambda d:
                            # datetime.datetime.strptime(d, "%Y-%m-%d")})
dfMeteoMilano = pd.read_csv('MeteoMilano.csv', parse_dates=['CET'])
print(dfMeteoMilano.info())

figTemp = plt.figure(figsize=(15, 9))
ax = figTemp.add_axes([0.1, 0.05, 0.85, 0.9])
ax.plot(dfMeteoMilano['Temperatura minC'])
plt.savefig('meteoMilanoSimplePlot.pdf', format='pdf',
            orientation='landscape', transparent=True)

# refining it

figTemp = plt.figure(figsize=(15, 9))
ax = figTemp.add_axes([0.1, 0.05, 0.85, 0.9])
ax.plot(dfMeteoMilano['CET'][:1000],
        dfMeteoMilano['Temperatura minC'][:1000],
        ls='None',
        marker='o')
plt.savefig('meteoMilanoSimplePlotX.pdf', format='pdf',
            orientation='landscape', transparent=True)


figTemp = plt.figure(figsize=(15, 9))
ax = figTemp.add_axes([0.1, 0.05, 0.85, 0.9])
plt.fill_between(np.arange(1000), dfMeteoMilano['Temperatura minC'][:1000],
                 dfMeteoMilano['Temperatura maxC'][:1000], color='r', alpha=0.5)
plt.plot(np.arange(1000), dfMeteoMilano['Temperatura mediaC'][:1000])
plt.savefig('meteoMilanoFill.pdf', format='pdf',
            orientation='landscape', transparent=True)

figTemp = plt.figure(figsize=(15, 9))
ax = figTemp.add_axes([0.1, 0.05, 0.85, 0.9])
plt.fill_between(np.arange(1000), dfMeteoMilano['Temperatura mediaC'][:1000],
                 dfMeteoMilano['Temperatura maxC'][:1000], color='r', alpha=0.5)
plt.fill_between(np.arange(1000), dfMeteoMilano['Temperatura mediaC'][:1000],
                 dfMeteoMilano['Temperatura minC'][:1000], color='b', alpha=0.5)
plt.plot(np.arange(1000),
         dfMeteoMilano['Temperatura mediaC'][:1000], c='k', alpha=0.25)
ax.set_xlabel('osservazione', fontsize=16)
ax.set_ylabel('[gradi C]', fontsize=16)
plt.savefig('meteoMilanoFill.pdf', format='pdf',
            orientation='landscape', transparent=True)
