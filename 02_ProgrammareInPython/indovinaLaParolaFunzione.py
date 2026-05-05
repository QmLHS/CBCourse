import numpy as np


def loadFile(fileName):
    with open(fileName, "r") as fileParole:
        lParole = fileParole.readlines()
        fileParole.close()
    return lParole


def estraiParola(lParole):
    rng = np.random.default_rng()
    lunghezzaLista = len(lParole)
    # estrai una parola
    iParola = rng.integers(0, lunghezzaLista - 1)
    parolaScelta = lParole[iParola]
    # print(parolaDaIndovinare)
    return parolaScelta.strip()


def fornisciAiuto(pTentativo, pDaIndovinare):
    conteggio = {}
    for carattere in pTentativo:
        if carattere not in conteggio.keys():
            conteggio[carattere] = pDaIndovinare.count(carattere)
    print("aiuto:")
    for el in conteggio.keys():
        print(el, "e' presente ", conteggio[el], "volte")


def verificaInserimento(pTentativo, pDaIndovinare, stop=False, guessed=False):
    if pTentativo == "-1":
        stop = True
    else:
        if pTentativo == pDaIndovinare:
            print("hai indovinato")
            guessed = True
        else:
            fornisciAiuto(pTentativo, pDaIndovinare)
    return (stop, guessed)


fileName = "listaParoleIta.txt"
listaParole = loadFile(fileName)

parolaDaIndovinare = estraiParola(listaParole)
print(parolaDaIndovinare)
print("la parola è composta da ", len(parolaDaIndovinare), "caratteri")

termina = False
indovinato = False
while termina is False and indovinato is False:
    parolaTentativo = input("che parola è? (-1 per terminare) ")
    termina, indovinato = verificaInserimento(
        pTentativo=parolaTentativo, pDaIndovinare=parolaDaIndovinare
    )
