import numpy as np

fileName = "listaParoleIta.txt"

with open(fileName, "r") as fileParole:
    listaParole = fileParole.readlines()
    fileParole.close()
lunghezzaLista = len(listaParole)

# estrai una parola
rng = np.random.default_rng()
iParola = rng.integers(0, lunghezzaLista - 1)
parolaDaIndovinare = listaParole[iParola]
# print parolaDaIndovinare
print("la parola è composta da ", len(parolaDaIndovinare), "caratteri")

termina = False
indovinato = False

while termina == False and indovinato == False:
    parolaTentativo = input("che parola è? (-1 per terminare) ")
    if parolaTentativo == "-1":
        termina = True
    else:
        if parolaTentativo == parolaDaIndovinare:
            print("hai indovinato")
            indovinato = True
        else:
            conteggio = {}
            for carattere in parolaTentativo:
                if carattere not in conteggio.keys():
                    conteggio[carattere] = parolaDaIndovinare.count(carattere)
            print("aiuto:")
            for el in conteggio.keys():
                print(el, "e' presente ", conteggio[el], "volte")
