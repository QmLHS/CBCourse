# Exercises — BLAST: Sequence Similarity Search

**Covered lecture:** L12_a

**Datasets** (inside `05_Sequences/data/`):

| File | Notes |
|------|-------|
| `DRR076693.3.fasta` | Single FASTA record (~522 bp), read #3 from *S. cerevisiae* S288c RNA-seq run DRR076693 |
| `DRR076693.fastq` | FASTQ file with multiple reads from the same run |
| `blastOutput_DRR076693.3.xml` | Pre-computed BLASTX result (query: `DRR076693.3.fasta`, program: `blastx`, db: `refseq_protein`) |

---

## Exercise 1 — Explore a FASTA record (difficulty: ★)

Load the file `data/DRR076693.3.fasta` using `SeqIO.read` and inspect its content.

1. Print the sequence **ID** and **description**.
2. Print the **length** of the sequence (in bp).
3. Print the **first 60 bases**.
4. Compute and print the **GC content** (percentage of G and C bases, rounded to 2 decimal places).

**Expected output (approximate):**

```
ID: DRR076693.3
Description: DRR076693.3 ...
Length: 522
First 60 bases: ATGC...
GC content: 42.34 %
```

**Hint:** GC content = `(seq.count('G') + seq.count('C')) / len(seq) * 100`

### Solution

<details>
<summary>Show solution</summary>

```python
from Bio import SeqIO

record = SeqIO.read('data/DRR076693.3.fasta', 'fasta')

print('ID:', record.id)
print('Description:', record.description)
print('Length:', len(record.seq))
print('First 60 bases:', record.seq[:60])

gc = (record.seq.count('G') + record.seq.count('C')) / len(record.seq) * 100
print(f'GC content: {gc:.2f} %')
```

</details>

---

## Exercise 2 — Remote BLASTN search (difficulty: ★★)

Using the sequence loaded in Exercise 1, run a **remote BLASTN** search against the `nt` database.

1. Call `NCBIWWW.qblast` with `program='blastn'`, `database='nt'`, and pass `record.format('fasta')` as the sequence.
2. Save the XML output to `data/blast_nucleotide.xml`.
3. Parse the saved file with `NCBIXML.read` and print the **number of alignments** returned.

**Note:** the remote search may take 1–5 minutes. Save the XML immediately so you do not need to repeat it.

**Hint:** use `with open(..., 'w') as f: f.write(result.read())` before closing the handle.

### Solution

<details>
<summary>Show solution</summary>

```python
from Bio import SeqIO
from Bio.Blast import NCBIWWW, NCBIXML

record = SeqIO.read('data/DRR076693.3.fasta', 'fasta')

blast_result = NCBIWWW.qblast(
    'blastn',
    'nt',
    record.format('fasta'))

with open('data/blast_nucleotide.xml', 'w') as f:
    f.write(blast_result.read())
blast_result.close()

with open('data/blast_nucleotide.xml', 'r') as f:
    blast_record = NCBIXML.read(f)

print('Number of alignments:', len(blast_record.alignments))
```

</details>

---

## Exercise 3 — Parse a BLASTX result (difficulty: ★★★)

The file `data/blastOutput_DRR076693.3.xml` contains a pre-computed BLASTX result
(query: `DRR076693.3.fasta`, database: `refseq_protein`).

1. Parse it with `NCBIXML.read`.
2. For **each hit** print: accession, description (first 60 characters), sequence length, and best E-value (i.e. the E-value of the first HSP).
3. **Filter**: keep only hits with best E-value `< 1e-10`. Print how many hits pass the filter.

**Expected output format:**

```
NP_014544.3 | YBR072W-A hypothetical protein ... | len=312 | E=2.3e-45
...
Hits with E-value < 1e-10: 8
```

**Hint:** `hit.hsps[0].expect` gives the E-value of the best HSP for that hit.

### Solution

<details>
<summary>Show solution</summary>

```python
from Bio.Blast import NCBIXML

with open('data/blastOutput_DRR076693.3.xml', 'r') as f:
    blast_record = NCBIXML.read(f)

filtered = []
for hit in blast_record.alignments:
    best_evalue = hit.hsps[0].expect
    desc = hit.hit_def[:60]
    print(f'{hit.accession} | {desc} | len={hit.length} | E={best_evalue:.2e}')
    if best_evalue < 1e-10:
        filtered.append(hit)

print(f'\nHits with E-value < 1e-10: {len(filtered)}')
```

</details>

---

## Exercise 4 — Fetch organism names and build a DataFrame (difficulty: ★★★)

Using the filtered hits from Exercise 3 (E-value `< 1e-10`):

1. For each hit, use `Entrez.efetch` to retrieve the **organism name**:
   - `db='protein'`, `id=hit.accession`, `rettype='gp'`, `retmode='xml'`
   - Extract `rec[0][0]['GBSeq_organism']`
2. Build a **pandas DataFrame** with columns: `ncbi_id`, `description`, `length`, `evalue`, `organism`.
3. Print the DataFrame.
4. Save it to `data/blast_results.xlsx` (without the row index).

**Hint:** collect one dictionary per hit in a list, then call `pd.DataFrame(rows)`.

### Solution

<details>
<summary>Show solution</summary>

```python
from Bio.Blast import NCBIXML
from Bio import Entrez
import pandas as pd

Entrez.email = 'nome@esempio.it'

with open('data/blastOutput_DRR076693.3.xml', 'r') as f:
    blast_record = NCBIXML.read(f)

filtered = [h for h in blast_record.alignments
            if h.hsps[0].expect < 1e-10]

rows = []
for hit in filtered:
    h = Entrez.efetch(
        db='protein', id=hit.accession,
        rettype='gp', retmode='xml')
    rec = Entrez.read(h)
    organism = rec[0][0]['GBSeq_organism']
    rows.append({
        'ncbi_id':     hit.accession,
        'description': hit.hit_def,
        'length':      hit.length,
        'evalue':      hit.hsps[0].expect,
        'organism':    organism,
    })

df = pd.DataFrame(rows)
print(df)
df.to_excel('data/blast_results.xlsx', index=False)
```

</details>

---

## Exercise 5 — BLASTX on a FASTQ read (difficulty: ★★★★)

Run a BLASTX search for a **different** sequence taken from the FASTQ file.

1. Open `data/DRR076693.fastq` with `SeqIO.parse` (format `'fastq'`) and retrieve the **second record** (index 1).
2. Convert it to a FASTA-format string using `record.format('fasta')` and pass it to `NCBIWWW.qblast` with `program='blastx'`, `database='refseq_protein'`.
3. Save the XML to `data/blast_read2.xml`.
4. Parse the result. Filter hits with E-value `< 1e-5`.
5. For each filtered hit, extract the organism name with `Entrez.efetch` (as in Exercise 4).
6. Report: how many **unique organisms** appear among the top hits?

**Hint:** to get the second record from a generator use `next` twice, or convert to a list with `list(SeqIO.parse(...))`.

### Solution

<details>
<summary>Show solution</summary>

```python
from Bio import SeqIO, Entrez
from Bio.Blast import NCBIWWW, NCBIXML

Entrez.email = 'nome@esempio.it'

records = list(SeqIO.parse('data/DRR076693.fastq', 'fastq'))
read2 = records[1]
print('Using read:', read2.id, 'length:', len(read2.seq))

blast_result = NCBIWWW.qblast(
    'blastx',
    'refseq_protein',
    read2.format('fasta'))

with open('data/blast_read2.xml', 'w') as f:
    f.write(blast_result.read())
blast_result.close()

with open('data/blast_read2.xml', 'r') as f:
    blast_record = NCBIXML.read(f)

filtered = [h for h in blast_record.alignments
            if h.hsps[0].expect < 1e-5]

organisms = set()
for hit in filtered:
    h = Entrez.efetch(
        db='protein', id=hit.accession,
        rettype='gp', retmode='xml')
    rec = Entrez.read(h)
    org = rec[0][0]['GBSeq_organism']
    organisms.add(org)

print(f'Hits with E-value < 1e-5: {len(filtered)}')
print(f'Unique organisms: {len(organisms)}')
for org in sorted(organisms):
    print(' -', org)
```

</details>
