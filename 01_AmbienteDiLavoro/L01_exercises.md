# Doodling around bash


## Fetching data

Using `wget` retrive the genomic information at [https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_genomic.gff.gz](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_genomic.gff.gz)

`wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_genomic.gff.gz`

## Inspecting the file

We would like to inspect the file with `bat` to understand its structure, but the file is compressed.

If you use `gunzip` to decompress it

```bash
gunzip -c filename.gz
```
we will end up with a huge file.

We can inspect it without writing on the hard disk exploiting a pipeline:

```bash
gunzip -c GCF_000001405.40_GRCh38.p14_genomic.gff.gz | bat -A
```

If you prefer you can work on the first 30 lines of the file. Again, use a pipeline:

```bash
gunzip -c GCF_000001405.40_GRCh38.p14_genomic.gff.gz | head -n 30 | bat -A
```

It is a tab separated file i.e. in the tsv file format. We can exploit this to improve the output of bat:


```bash
gunzip -c GCF_000001405.40_GRCh38.p14_genomic.gff.gz | head -n 30 | bat -l tsv
```

We can see that a gene can be identified by the word gene in the third column.


## Extract the information

Let's imagine we want to count the number of genes.
Having inspected the file we can recognize that gene are identified by the word gene in the third position:


```bash
gunzip -c GCF_000001405.40_GRCh38.p14_genomic.gff.gz | rg "\tgene\t" | bat -l tsv
```
the `\t` around the `gene` string are the columns separators, so we exploit this to force the word gene to be the only in the column

It seems we catch it correctly.

Let's now count the lines in the file by means of `wc -l`


```bash
gunzip -c GCF_000001405.40_GRCh38.p14_genomic.gff.gz | rg "\tgene\t" | wc -l
```

How many genes are there? 

They are too much...

Looking at the second column we want to restrict to those lines having only `BestRefSeq`:


```bash
gunzip -c GCF_000001405.40_GRCh38.p14_genomic.gff.gz | rg "\tBestRefSeq\t" | rg "\tgene\t" | bat -l tsv
```

it works, let's count:

```bash
gunzip -c GCF_000001405.40_GRCh38.p14_genomic.gff.gz | rg "\tBestRefSeq\t" | rg "\tgene\t" | wc -l
```

Almost 20K is a closer guess.

