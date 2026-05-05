## 1. Caricare il contenuto del foglio excel "Grezzi.xls" in un dataframe dove siano presenti tutte le serie temporali associate ai vari esperimenti.

## 2. Ridurre il numero di colonne del dataframe a solo quelle di interesse: 'exp', 'time', 'OD'

## 3. Individuare le eventuali osservazioni che hanno valore NaN per la variabile OD ed eventualmente eliminarle


## 4. Aggiungere al dataframe una nuova colonna contentente l'etichetta della fonte di nutrimento utilizzata.
# Vediamo cosa ci dice il nome dell'esperimento. Ha una struttura?
# La struttura è EXPTag+Fonte+Progressivo i.e. AGlut2: exp A, fonte Glutammato, secondo esperimento
#         exp  time      OD fonte
# 287   JAmm2  22.0   3.950   Amm
# 48    CGlut   1.5   0.235  Glut
# 235   IAmm1  55.0   5.030   Amm
# 25    BGlut  32.0   2.440  Glut
# 113  EGlut2  21.5   0.193  Glut
# 219   HAmm2   4.5   0.970   Amm
# 250   IAmm2  72.0   5.360   Amm
# 149    FAmm   4.5   1.200   Amm
# 143   FGlut  31.0  21.800  Glut
# 222   HAmm2  24.0   6.900   Amm

# Con regular expressions [regex101: build, test, and debug regex](https://regex101.com/) :

# Ora Possiamo separare gli esperimenti in base alla fonte nutrititva

# Controlliano le dimensioni per verificare di non aver perso osservazioni:

# it is possible to describe a population growth by means of the sigmoid (logistic) function.
# We can leverage the definition of a python function to draw such a function:
# [Logistic function - Wikipedia](https://en.wikipedia.org/wiki/Logistic_function)
def sigmoid(xIn, yMax, xMidpoint, kSteep):
    return yMax / (1.0 + np.exp(-kSteep * (xIn - xMidpoint)))



# Per tentare di allineare le serie temporali, si potrebbe tentare di fittare ciascuna curva con una sigmoide e sfruttare il xMidPont per traslare i tempi di ciascuna curva


