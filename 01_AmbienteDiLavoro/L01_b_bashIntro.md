# Virtual Machine, terminale, bash e interazione con il file system


## Accedere alla virtual machine (VM)


1. Utilizzare il seguente link per accedere ai laboratori LIBasS a cui siete registrati

    [https://libaas-lessons.si.unimib.it/](https://libaas-lessons.si.unimib.it/)

    ![Scelta della modalità di accesso](/Users/dario/gDrive/Images/vmInfo@SGI_LIBasS_01_SceltaModalita.png "Modalità di accesso"){#id .class width=30%}

    * **"Horizon Client"** si accede tramite client istallato sulla vostra macchina
    * **"HTML Access"** si accede tramite il browser web


2. Vi verrà chisesti di autenticarvi tramite le credenziali CAS d'Ateneo:

    usate il vostro account d'Ateneo **`nomeUtente@campus.unimib.it`**

    ![Autenticazione accesso VM](/Users/dario/gDrive/Images/vmInfo@SGI_LIBasS_02_Autenticazione.png "Autenticazion accesso VM"){#id .class width=30%}

3. Selezionate la macchina `libaas1171` clicckando sull'icona per accedervi.

    ![Scelta VM](/Users/dario/gDrive/Images/vmInfo@SGI_LIBasS_03_SceltaVM.png "Scelta VM")


4. Una volta che la macchina è in esecuzione dovreste vedere una schermata simile all'immagine che segue

    ![Scelta VM](/Users/dario/gDrive/Images/vmInfo@SGI_LIBasS_04_RemoteDesktop.png "VM in esecuzione")

5. **Ricordate sempre di disconnettervi dalla macchina al termine del suo utilizzo.**

Per ulteriori informazioni sono a disposizione le seguenti guide:

* [LIBaaS - Horizon - Guida all'accesso - HTML5](https://sites.google.com/unimib.it/libaas-horizon/guida-allaccesso-html5)
* [LIBaaS - Horizon - Guida all'accesso - Client](https://sites.google.com/unimib.it/libaas-horizon/guida-allaccesso-client)


## Condividere i file con la VM

Con un doppio click sull'icona che trovate sul Desktop,

  ![montare gDrive](/Users/dario/gDrive/Images/infoStatVMmountGDrive.png "montare gDrive"){#id .class width=30%}

 potrete "montare" il file system di google drive in locale:

  ![accessibile localmente](/Users/dario/gDrive/Images/infoStatVMgDriveTree.png "accessibile localmente")


## Accedere al terminale

Dal desktop clickare sull'icona in basso a sinistra per aprire il menù di accesso alle applicazioni:

![aprire ricerca applicazioni](/Users/dario/gDrive/Images/infoStatVMavviareApplicazioni.png "aprire ricerca applicazioni")

scrivere terminale nella barra di ricerca:

![ricerca applicazioni](/Users/dario/gDrive/Images/infoStatVMcercaApplicazione.png "ricerca applicazioni")

ora potete interagire con il terminale:

![terminale](/Users/dario/gDrive/Images/infoStatVMterminale.png "terminale")

____


## Come chiedere aiuto

`man` il manuale di ciascun comando



## Come muoversi nel file system

* `pwd` - dove mi trovo?
* `ls` - cosa trovo?
* `cd` - portami lì!
* `tab` per il completamento automatico
* altri aiuti per lo storico dei comandi



## Percorsi assoluti e relativi

**slides from Info@Stat**

* `/` radice (e separatore delle directory)
* `~` home
* `.` qui
* `..` su di uno
* `-` portami indietro
* `*` quello che vuoi

## Lavorare con i file: i primi passi

## `mkdir`  crea una nuova directory

##### *Esempio*:

crea una nuova directory chiamata E01. All'interno di E01 create due nuove directory chiamate d01 e d02

```bash
  mkdir E01
  cd E01/
  mkdir d01
  mkdir d02
```

##### *Esercizio*:
crea una nuova directory `d02Sub` all'interno della directory `d02`



## `mv` muovi il file

#### *Esempio*:
muovere il file `file01` dalla directory `d01` alla directory `d02`

```bash
  mv d01/file01 d02/
```

####  *Esercizio*:
muovere il file `file01` dalla directory `d02` alla directory `d02Sub`



## `cp` copia il file

#### *Esempio*:
copia il file `file01` contenuto in d02Sub nella directory `d01`

```bash
  cp d02/d02Sub/file01 d01/
```

#### *Esercizio*:
copia il file `file01`  contenuto in d01 nella directory `d02`




## `cat` cosa c'è dentro? (stampa a video del contenuto)

#### *Esempio*:
stampa a video il contenuto del file `file01` contenuto nella directory `d01`

```bash
 cat d01/file01
```

#### *Esercizio*:
stampa a video il contenuto del file `file01` contenuto nella directory `d02Sub`



## `less` leggere il contenuto di un file ... con calma

#### *Esempio*:
leggi il contenuto del file `file01` contenuto nella directory `d01`

```bash
  less d01/file01
```

#### *Esercizio*:
leggi il contenuto del file `file01` contenuto nella directory `d02Sub`

## `head`  stampami le prime righe del file

#### *Esempio*:
stampa le prime due righe del file `file01` contenuto nella directory `d01`

```bash
  head -n 2 d01/file01
```

#### *Esercizio*:
stampa le prime righe del file `file01` contenuto nella directory `d02Sub`




## `tail` stampami le ultime righe del file

#### *Esempio*:
stampa le ultime due righe del file 'file01' contenuto nella directory `d01`

```bash
  tail -n 2 d01/file01
```

#### *Esercizio*:
stampa le ultime righe del file `file01` contenuto nella directory `d02Sub`

## `|` (pipe) combina due o più comandi

#### *Esempio*:
seleziona le prime 5 righe del file `file01` contenuto nella directory `d01` e stampa a video le ultime 2 righe

```bash
  cat d01/file01 | head -5 | tail -2
```

#### *Esercizio*:
seleziona le ultime 6 righe del file `file01` contenuto nella directory `d02Sub` e stampa a video le ultime 2 righe

## `rm`, `rmdir` cancella file e directory o solo directory

#### *Esempio*:
rimuovi il file `file01` in d01 e la directory `d02Sub` con tutto il suo contenuto

```bash
  mkdir d02/d02Sub02
  rm d01/file01
  rmdir d02/d02Sub02
  rm -r d02/d02Sub
```

#### *Esercizio*:
rimuovi tutto il contenuto della directory d02




## `zip` e `unzip` (`tar`, `bz2`, ...)

#### *Esempio*:
comprimi la directory E01 e tutto il suo contenuto. Successivamente decomprimi la directory E01.zip appena creata.

```bash
  zip -r E01.zip E01
  unzip E01.zip
 ```

#### *Esercizio*:
comprimi la directory d02Sub e tutto il suo contenuto. Successivamente decomprimi la directory d02Sub.zip appena creata.

# più avanzato

## `touch` crea file vuoti..

#### *Esempio*:
crea un file vuoto chiamato 'file01' nella directory d01

```bash
  touch d01/file01
```

####  *Esercizio*:
crea un file vuoto chiamato 'file02' nella directory d02Sub

## `chown` cambia il propietario, il gruppo etc. del file

#### *Esempio*:
cambia l'utente proprietario e il gruppo assegnato alla directory E01

```bash
  chown nomeproprietario:nomegruppo E01/
```

## `chmod` cambia i permessi del file

#### *Esempio*:
assegnare per la directory E01: al proprietario tutti i permessi, al gruppo solo lettura ed esecuzione (ma non scrittura) ed agli altri utenti nulla.

```bash
  chmod 750 nomefile
```



## `grep` -> `rg` trovami tutti i file che contengono una stringa

#### *Esempio*:
trova nella directory d01 tutti i file contenenti il carattere @

```bash
  rg @ d01/
```

#### *Esercizio*:
trova nella directory d02Sub tutti i file contenenti il carattere '-'



## `find` -> `fdfind`, `fd` trovami tutti i file che contengono una stringa nel nome

#### *Esempio*:
trova nella directory d01 tutti i file il cui nome inizia con il carattere 'f' e termina con la stringa '01'

```bash
  find ./d01/ -name 'f*01'
```

## `wc` contami le righe, i caratteri, le parole, ....

#### *Esempio*:
conta il numero di righe del file 'file01' contenuto nella directory d01

```bash
  wc -l d01/file01
```

####  *Esercizio*:

conta il numero di righe del file 'file01' contenuto nella directory d02Sub



## `>`, `>>` scrivi in un file

#### *Esempio*:
conta il numero di righe del file 'file01' contenuto nella directory d01 e stampa il messaggio di output in un file chiamato numeroRighe01

```bash
  wc -l d01/file01 > numeroRighe01
```

####  *Esercizio*:
conta il numero di righe del file 'file01' contenuto nella directory d02Sub  e stampa il messaggio di output in un file chiamato numeroRighe02


## `htop` cosa sta girando sul mio pc?

`htop`

____


# Caccia al TESORO

Decomprimi il file CacciaAlTesoro.zip e usa i comandi spiegati precedentemente per trovare il tesoro.

Il punto di partenza è il file non vuoto in `laForesta`

____


# Usare Python

* `python` modalità interattiva
* `python nomeSorgente.py` per eseguire il programma "nomeSorgente.py"
