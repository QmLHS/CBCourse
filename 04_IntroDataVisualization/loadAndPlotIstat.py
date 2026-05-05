import matplotlib.pyplot as plt


colorDict = {
    'red': '#FF1A1C',
    'blue': '#377EB8',
    'green': '#4DAF4A',
    'purple': '#984EA3',
    'orange': '#FF7F00',
    'yellow': '#FFFF33',
    'brown': '#A65628',
    'pink': '#F267B2'
}

fileName = 'ita-Popolazione_per_eta_-_Ripartizione_Italia2017.csv'

# il più semplice = meno automatico
with open(fileName, 'r') as stream:
    linee = stream.readlines()
    stream.close()
# print(linee[:10])


dizAnni = {}

for linea in linee:
    riga = linea.strip()
    if riga[0] == '"':  # righe di intestazione
        if riga[0:len('"Anno:')] == '"Anno:':
            tokens = riga.split('-')
            infoAnno = tokens[0].strip()
            anno = int(infoAnno.split(':')[1].strip())
            # print(anno)
            dizAnni[anno] = {}
        elif riga[0:len('"Maschi"')] == '"Maschi"':
            genere = 'maschi'
            dizAnni[anno][genere] = {}
        elif riga[0:len('"Femmine"')] == '"Femmine"':
            genere = 'femmine'
            dizAnni[anno][genere] = {}
        elif riga[0:len('"Totale"')] == '"Totale"':
            genere = 'totale'
            dizAnni[anno][genere] = {}
    else:
        tokens = riga.split(';')
        # print(tokens)
        eta = tokens[0]
        if eta != '110 e oltre' and eta != 'Totale':
            dizAnni[int(anno)][genere][int(eta)] = int(tokens[4])
        elif eta == '110 e oltre':
            dizAnni[int(anno)][genere][110] = int(tokens[4])
        else:
            # print(tokens[0], int(tokens[4]))
            pass


# print(dizAnni[2017]['maschi'][0])
# print(dizAnni[2017]['femmine'][0])


fig, ax = plt.subplots()
ax.barh(list(dizAnni[2017]['maschi'].keys()), list(
    dizAnni[2017]['maschi'].values()),
    align='center', color=colorDict['blue'])
# ax.set_yticks(valoriEta)
plt.title('Distribuzione delle età nel 2017')
plt.xlabel('Numerosità')
plt.ylabel('età')
plt.savefig('distribEtaMaschi2017.svg')

lPlotSx = []
for el in list(dizAnni[2017]['femmine'].values()):
    lPlotSx.append(-el)
fig, ax = plt.subplots()
g1 = ax.barh(list(dizAnni[2017]['maschi'].keys()), list(
    dizAnni[2017]['maschi'].values()),
    align='center')
g2 = ax.barh(list(dizAnni[2017]['femmine'].keys()), lPlotSx,
             align='center')
# ax.set_yticks(valoriEta)
plt.savefig('distribEta2017Bare.svg')


valoriEta = list(dizAnni[2017]['maschi'].keys())
fig, ax = plt.subplots()
g1 = ax.barh(valoriEta, list(dizAnni[2017]['maschi'].values()),
             align='center', color=colorDict['blue'])
g2 = ax.barh(valoriEta, lPlotSx,
             align='center', color=colorDict['pink'])
ax.grid(False)
ax.set_frame_on(False)
plt.title('Distribuzione delle età nel 2017', fontsize=16)
plt.xlabel('Numerosità', fontsize=12)
plt.ylabel('età', fontsize=12)
plt.legend((g1[0], g2[0]), ('maschi', 'femmine'))
plt.xticks([-4e5, -2e5, 0, 2e5, 4e5])
ax.set_xticklabels(['4e5', '2e5', '0', '2e5', '4e5'], fontsize=10)
plt.savefig('distribEta2017.svg')


lPlotSx50 = []
for el in list(dizAnni[2050]['femmine'].values()):
    lPlotSx50.append(-el)
fig, ax = plt.subplots()
g1 = ax.barh(valoriEta, list(dizAnni[2017]['maschi'].values()),
             align='center', color=colorDict['blue'], alpha=0.5)
g2 = ax.barh(valoriEta, lPlotSx,
             align='center', color=colorDict['pink'], alpha=0.5)
g3 = ax.barh(valoriEta, list(dizAnni[2050]['maschi'].values()),
             align='center', color=colorDict['green'], alpha=0.5)
g4 = ax.barh(valoriEta, lPlotSx50,
             align='center', color=colorDict['purple'], alpha=0.5)
ax.grid(False)
ax.set_frame_on(False)
plt.title('Variazione della distribuzione delle popolazioni dal 2017 al 2050',
          fontsize=12)
plt.xlabel('Numerosità', fontsize=11)
plt.ylabel('età', fontsize=11)
plt.legend((g2[0], g4[0], g1[0], g3[0]),
           ('2017 F', '2050 F', '2017 M', '2050 M'), ncol=2, fontsize=8)
plt.xticks([-4e5, -2e5, 0, 2e5, 4e5])
ax.set_xticklabels(['4e5', '2e5', '0', '2e5', '4e5'], fontsize=10)
plt.savefig('distribEta2017_50.pdf')
