# -*- coding: utf-8 -*-
# il commento sopra serve per le lettere accentate,
# per favore non modificate queste prime righe

nomeEsercizio = 'fasta'

##########################################################
# INTRODUZIONE
##########################################################
#
# Il processo dell'espressione genica è al centro della vita
# e riguarda il mantenimento e la trasmissione dell'informazione
# negli esseri viventi. Questo processo si sviluppa in tre fasi,
# conservazione, trascrizione, traduzione e ruota intorno a tre
# macromolecole, DNA, RNA e proteine. Per accedere alla comprensione
# dei meccanismi molecolari all'interno della cellula è necessario
# studiare l'espressione genica con strumenti informatici.
# Il programma che vi è richiesto implementare replicherà le ultime
# due fasi dell'espressione genica per alcune sequenze geniche.
# La fase di trascrizione 'trasforma' la sequenza di nucleotidi {A,C,G,T}
# contenuta nel DNA nella corrispondente sequenza di nucleotidi {A,C,G,U}
# del RNA. Attenzione: ciascuna base 'T' viene convertita in una base 'U'.
# Nella fase di traduzione, l'RNA viene letto per triplette (stringa di tre
# elementi, anche chiamate codoni) e a ciascuna tripletta viene associata il
# corrispondente aminoacido secondo un preciso dizionario. La catena di aminoacidi
# così composta forma una proteina.


##########################################################
# DESCRIZIONE DEI FILE CON I DATI
##########################################################
#
# Nel file .zip troverete i seguenti file, oltre a questo script:
#
# - File 1) ls_orchid.fasta
#   Il file contiene alcune sequenze genomiche di RNA codificate nel formato
#   FASTA. In questo formato, a ciascuna sequenza è associata una riga di
#   intestazione (defline) identificata dal carattere '>' in cui vengono
#   memorizzate le informazioni che accompagnano la sequenza a cui fanno
#   seguito una o più righe che contengono la sequenza di nucleotidi che
#   costituiscono il gene. Ciascuna sequenza termina con una riga vuota.
#
#   Per ogni sequenza la defline ha il seguente formato:
#   gi|numero-gi|emb|accession|locus commenti
#   dove:
#   * numuro-gi è il valore numerico associato alla sequenza nell base di dati
#   * emb è l'identificativo della base di dati da cui è stata recuperata l'informazione
#   * accession è un identificativo alternativo per la sequenza
#   * locus è la posizione sul genoma
#   * commenti sono le informazioni aggiuntive a corredo della sequenza
#   Un'intestazione di esempio è la seguente:
#   >gi|2765658|emb|Z78533.1|CIZ78533 C.irapeanum 5.8S rRNA gene and ITS1 and ITS2 DNA
#
#   Le righe che seguono la defline contengono la sequenza di nucleotidi, possono
#   avere lunghezza variabile e contenere caratteri diversi da {'A','C','G','T'}
#
# - File 2) codonTable.txt
#   Questo file contiene le informazioni per il processo di traduzione dai nucleotidi
#   agli aminoacidi e quindi alla formazione delle proteine.
#
#   Ogni riga contiene due colonne separate dal simbolo di tabulazione '\t':
#   * tripletta di nucleotidi
#   * aminoacido associato
#
# Provate ad aprire i file con un editor di testi.
# State attenti, se aprirete il file con Excel o con il
# notepad di windows, alcune informazioni potrebbero essere
# VISUALIZZATE in MANIERA DISTORTA rispetto al contenuto del file.


##########################################################
# DESCRIZIONE DEL LAVORO DA SVOLGERE
##########################################################
#
# Implementate le seguenti funzioni, il commento che precede
# ogni funzione vi spieghera' cosa fare in dettaglio.
# Controllate nel corpo principale del programma (in fondo
# allo script), come vengono invocate le funzioni che
# implementerete.
# Per favore NON USATE le istruzioni input() o raw_input()
# nel codice che scriverete.
# Se volete potete implementare delle funzioni aggiuntive
# rispetto a quelle gia' presenti qua sotto.

##########################################################
# INIZIO DELLA PARTE DA EDITARE
##########################################################

cognome = 'Sostituiscimi con il cognome'  # inserisci qua il tuo cognome
nome = 'Sostituiscimi con il nome'  # inserisci qua il tuo nome

# - caricaSeqs(filename). La funzione accetta come unico parametro in
#   ingresso il nome del file con contenente le sequenze.
#   La funzione deve restituire un dizionario di dizionari, dove il dizionario
#   esterno contiene un elemento per ogni sequenza la cui chiave è il relativo
#   numero_gi mentre il relativo valore è un dizionario di quattro elementi così strutturato:
#   {'gi': numeroGI, 'emb': accessionGI, 'locus': locusECommenti, 'seq': sequenzaNucleotidica}
#   dove numeroGI, accessionGI, locusECommenti sono contenuti nella defline di
#   ciascuna sequenza, mentre sequenzaNucleotidica è la stringa ottenuta dalla
#   concatenazione delle stringhe contenute nelle successive righe della sequenza.
#   Il dizionario di dizionari avrà la seguente struttura:
#   { numeroGI_1:{'gi': numeroGI_1, 'emb': accessionGI_1, 'locus': locusECommenti_1,
#    'seq': sequenzaNucleotidica_1},
#   ...,
#   numeroGI_N:{'gi': numeroGI_N, 'emb': accessionGI_N, 'locus': locusECommenti_N,
#    'seq': sequenzaNucleotidica_N} }
#   Segue un esempio di coppia chiave valore per un elemento del dizionario di dizionari:
#   '2765658':{'gi':'2765658', 'emb':'Z78533.1', 'locus': 'CIZ78533 C.irapeanum 5.8S rRNA gene and ITS1 and ITS2 DNA', 'seq': 'CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGATGAGACCGTGGAATAAACGATCGAGTGAATCCGGAGGACCGGTGTACTCAGCTCACCGGGGGCATTGCTCCCGTGGTGACCCTGATTTGTTGTTGGGCCGCCTCGGGAGCGTCCATGGCGGGTTTGAACCTCTAGCCCGGCGCAGTTTGGGCGCCAAGCCATATGAAAGCATCACCGGCGAATGGCATTGTCTTCCCCAAAACCCGGAGCGGCGGCGTGCTGTCGCGTGCCCAATGAATTTTGATGACTCTCGCAAACGGGAATCTTGGCTCTTTGCATCGGATGGAAGGACGCAGCGAAATGCGATAAGTGGTGTGAATTGCAAGATCCCGTGAACCATCGAGTCTTTTGAACGCAAGTTGCGCCCGAGGCCATCAGGCTAAGGGCACGCCTGCTTGGGCGTCGCGCTTCGTCTCTCTCCTGCCAATGCTTGCCCGGCATACAGCCAGGCCGGCGTGGTGCGGATGTGAAAGATTGGCCCCTTGTGCCTAGGTGCGGCGGGTCCAAGAGCTGGTGTTTTGATGGCCCGGAACCCGGCAAGAGGTGGACGGATGCTGGCAGCAGCTGCCGTGCGAATCCCCCATGTTGTCGTGCTTGTCGGACAGGCAGGAGAACCCTTCCGAACCCCAATGGAGGGCGGTTGACCGCCATTCGGATGTGACCCCAGGTCAGGCGGGGGCACCCGCTGAGTTTACGC'}


def caricaSeqs(filename):
    dizSeqs = {}
    with open(filename, 'r') as fasta:
        for line in fasta:
            # print '-|' + line +'|-'
            if line[0] == '>':
                tokens = line[1:].strip().split('|')
                # print '\n\ndefline: ', tokens
                dizSeq = {'gi': tokens[1], 'emb': tokens[3], 'locus': tokens[4]}
                sequence = ''
                # print 'gi:\t', dizSeq['gi']
                # print 'emb:\t', dizSeq['emb']
                # print 'locus:\t', dizSeq['locus']
            elif line[0] == '\n':
                # print 'discard'
                dizSeq['seq'] = sequence
                dizSeqs[dizSeq['gi']] = dizSeq
            else:
                # print 'SEQline', line
                seq = line.strip()
                sequence += seq
                # print 'seq\t', sequence
        fasta.close()
        return dizSeqs

# - trascrizione(dnaSeq). La funzione accetta come unico parametro in
#   ingresso una stringa dnaSeq (che è la stringa associata alla chiave 'seq').
#   La funzione deve restituire la stringa rnaSeq, identica a dnaSeq ma in cui a
#   ciascun carattere 'T' viene sostituito il carattere 'U'.

def trascrizione(dnaSeq):
    rnaSeq = ''
    for base in dnaSeq:
        if base == 'T':
            rnaSeq += 'U'
        else:
            rnaSeq += base
    return rnaSeq

# - traduzione(filename). La funzione accetta come unico parametro in
#   ingresso il nome del file con contenente la tabella di conversione dai nucleotidi
#   agli aminoacidi.
#   La funzione deve restituire un dizionario contenente una coppia chiave valore
#   costruita da ogni riga del file. La chiave di ogni coppia sarà la stringa
#   di tre caratteri associata alla triplette di nucleotidi, mentre il valore
#   sarà la stringa associata all'aminoacido nel file.
#   Segue a titolo esemplificativo parte del dizionario:
#   {'GUC': 'V', 'AUA': 'I', ...,'UAA': 'STOP', 'GAU': 'D', 'UUC': 'F'}
def traduzione(filename):
    with open(filename, 'r') as codons:
        rna2cod = codons.readlines()
        codons.close()
    an2aa = {}
    for line in rna2cod:
        tokens = line.strip().split('\t')
        an2aa[tokens[0]] = tokens[1]
    # print an2aa
    return an2aa


# funzione necessaria per restringere ad alfabeto di soli AUCG
def checkRNA(rnaFrag):
    flag = True
    for base in rnaFrag:
        if base not in 'AUCG':
            flag = False
    return flag

def seq2protein(dSeqs, dCT):
    dSeqsProts = {}
    for seq in dSeqs:
        # print seq
        rnaString = trascrizione(dSeqs[seq]['seq'])
        # print rnaString
        prots = []
        for readFrame in range(3):
            prot = ''
            for i in range(readFrame, len(rnaString) - readFrame - 1, 3):
                codon = rnaString[i:i + 3]
                # print codon
                if len(codon) == 3 and checkRNA(codon):
                    protFrag = dCT[codon]
                    if protFrag == 'STOP':
                        prot += '*'
                    else:
                        prot += protFrag
            prots.append(prot)
        dSeqsProts[seq] = prots
    return dSeqsProts

##########################################################
# Fine del compito e della parte da editare obbligatoriamente
# Inizio del corpo principale del programma. Potete
# modificare o lasciare invariato il codice qua sotto
# (a vostra scelta), se lo modificate, accertatevi
# che il codice non dia errori in esecuzione.
##########################################################


print('Esercizio %s.' % (nomeEsercizio))

print('Ciao %s, %s .' % (nome, cognome))

print("1) Eseguo la funzione caricaSeqs('ls_orchid.fasta') ")
dizSequenze = caricaSeqs('ls_orchid.fasta')
print 'numero sequenze caricate: ', len(dizSequenze)
print dizSequenze['2765658']

print("2) Eseguo la funzione traduzione('codonTable.txt') ")
dizAN2AA = traduzione('codonTable.txt')
print dizAN2AA

print("2) Eseguo la funzione seq2protein(dizSequenze, dizAN2AA) ")
dizSeqsProteins = seq2protein(dizSequenze, dizAN2AA)
print  dizSeqsProteins

print('Nome dello script eseguito')
print(__file__)  # Questa istruzione stampa il nome dello script, ignoratela.
