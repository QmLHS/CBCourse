nFileParole = 'listaParoleIta.txt'
with open(nFileParole, 'r') as stream:
    lParole = stream.readlines()
    stream.close()

listaParole = list()
for parola in lParole:
    listaParole.append(parola.strip())
del listaParole[-1]
#  print(listaParole)

parolaDaRimare = input('Dimmi la parola di cui vuoi la rima ')
#  print(parolaDaRimare)
lunghezzaRima = int(input('Quanto deve essere lunga la rima? '))
print('la rima è: ' + parolaDaRimare[-lunghezzaRima:])

listaRime = list()
for parola in listaParole:
    if parola[-lunghezzaRima:] == parolaDaRimare[-lunghezzaRima:]:
        listaRime.append(parola)

print('Ho trovato ' + str(len(listaRime)) + ' rime')
for parola in listaRime:
    print(parola)
