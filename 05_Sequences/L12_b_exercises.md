# Exercises — Multiple Sequence Alignment

**Covered lecture:** L12_b

**Datasets** (inside `05_Sequences/data/`):

| File | Notes |
|------|-------|
| `multipleSequences.faa` | Protein sequences (FASTA) from the top BLAST hits of `DRR076693.3.fasta` against `refseq_protein` (~12 sequences) |
| `blastOutput_DRR076693.3.xml` | Pre-computed BLASTX result used to generate the sequences above |

**External tools required:**
- `clustalw2` — `conda install -c bioconda clustalw`
- `muscle` — `conda install -c bioconda muscle`

---

## Exercise 1 — Inspect the input sequences (difficulty: ★)

Load the file `data/multipleSequences.faa` using `SeqIO.parse` (format `'fasta'`).

1. Print the **total number of sequences**.
2. For each sequence print its **ID** and **length** (in amino acids).
3. Print the **ID of the longest sequence**.

**Expected output format:**

```
Number of sequences: 12
NP_014544.3  312 aa
XP_004178593.1  298 aa
...
Longest: NP_014544.3
```

**Hint:** `len(record.seq)` gives the length; collect lengths in a dictionary or list to find the maximum.

### Solution

<details>
<summary>Show solution</summary>

```python
from Bio import SeqIO

records = list(SeqIO.parse('data/multipleSequences.faa', 'fasta'))

print('Number of sequences:', len(records))

lengths = {}
for rec in records:
    print(f'{rec.id}  {len(rec.seq)} aa')
    lengths[rec.id] = len(rec.seq)

longest_id = max(lengths, key=lengths.get)
print('Longest:', longest_id)
```

</details>

---

## Exercise 2 — ClustalW alignment (difficulty: ★★)

Run a **ClustalW** alignment on `data/multipleSequences.faa`.

1. Use `ClustalwCommandline` with `infile='data/multipleSequences.faa'`.
2. Execute the command line object to run the alignment.
3. Read the resulting `.aln` file with `AlignIO.read` (format `'clustal'`).
4. Print:
   - the number of sequences in the alignment
   - the alignment length (including gaps)
   - the first **40 columns** of each sequence (ID and gapped sequence slice)

**Hint:** ClustalW writes output files in the same folder as the input file, with the same base name.

### Solution

<details>
<summary>Show solution</summary>

```python
from Bio.Align.Applications import ClustalwCommandline
from Bio import AlignIO

clustalw_cline = ClustalwCommandline(
    'clustalw2',
    infile='data/multipleSequences.faa')

stdout, stderr = clustalw_cline()

align = AlignIO.read('data/multipleSequences.aln', 'clustal')

print('Number of sequences:', len(align))
print('Alignment length:', align.get_alignment_length())

print('\nFirst 40 columns:')
for rec in align:
    print(f'{rec.id:<20} {rec.seq[:40]}')
```

</details>

---

## Exercise 3 — MUSCLE alignment (difficulty: ★★)

Run a **MUSCLE** alignment on the same input file and compare the result with ClustalW.

1. Use `MuscleCommandline` with `input='data/multipleSequences.faa'`.
2. Save output as FASTA to `data/muscleAlignment.afa`.
3. Run again with `clw=True` and `out='data/muscleAlignment.aln'` to get ClustalW-format output.
4. Read **both** output files with `AlignIO.read` (formats `'fasta'` and `'clustal'`).
5. Print the alignment length for each and check whether they are equal.

**Note:** the two MUSCLE runs may produce slightly different gap distributions depending on the version; the lengths should nevertheless match.

### Solution

<details>
<summary>Show solution</summary>

```python
from Bio.Align.Applications import MuscleCommandline
from Bio import AlignIO

# FASTA output
muscle_fasta = MuscleCommandline(
    'muscle',
    input='data/multipleSequences.faa',
    out='data/muscleAlignment.afa')
muscle_fasta()

# ClustalW output
muscle_clw = MuscleCommandline(
    'muscle',
    input='data/multipleSequences.faa',
    out='data/muscleAlignment.aln',
    clw=True)
muscle_clw()

align_fasta = AlignIO.read('data/muscleAlignment.afa', 'fasta')
align_clw   = AlignIO.read('data/muscleAlignment.aln', 'clustal')

len_fasta = align_fasta.get_alignment_length()
len_clw   = align_clw.get_alignment_length()

print('MUSCLE FASTA alignment length:', len_fasta)
print('MUSCLE ClustalW alignment length:', len_clw)
print('Equal:', len_fasta == len_clw)
```

</details>

---

## Exercise 4 — Read and colour a phylogenetic tree (difficulty: ★★★)

Work with the ClustalW guide tree produced in Exercise 2.

1. Read `data/multipleSequences.dnd` with `Phylo.read` (format `'newick'`).
2. Draw the tree in ASCII with `Phylo.draw_ascii`.
3. Identify the **first** and **last** sequence IDs in `data/multipleSequences.faa` (use `SeqIO.parse` to get them in order).
4. Convert the tree to PhyloXML with `tree.as_phyloxml()`.
5. Find the **most recent common ancestor** (MRCA) of those two sequences using `tree.common_ancestor`.
6. Set `mrca.color = 'blue'`.
7. Save the coloured tree to `data/tree_clustalw_coloured.xml` in PhyloXML format.

**Hint:** `Phylo.write(tree, filename, 'phyloxml')` saves in PhyloXML format.

### Solution

<details>
<summary>Show solution</summary>

```python
from Bio import SeqIO, Phylo

# Get first and last sequence IDs
records = list(SeqIO.parse('data/multipleSequences.faa', 'fasta'))
first_id = records[0].id
last_id  = records[-1].id
print('First:', first_id, '  Last:', last_id)

# Read and display tree
tree = Phylo.read('data/multipleSequences.dnd', 'newick')
Phylo.draw_ascii(tree)

# Convert to PhyloXML and colour the MRCA clade
tree = tree.as_phyloxml()
mrca = tree.common_ancestor({'name': first_id}, {'name': last_id})
mrca.color = 'blue'

# Save
Phylo.write(tree, 'data/tree_clustalw_coloured.xml', 'phyloxml')
print('Saved coloured tree to data/tree_clustalw_coloured.xml')
```

</details>

---

## Exercise 5 — Full pipeline: BLAST hits to side-by-side phylogenetic trees (difficulty: ★★★★)

Combine all steps learned in L12_a and L12_b into a single pipeline.

1. **Parse** `data/blastOutput_DRR076693.3.xml` with `NCBIXML.read`.
2. Take the **top 8 hits** (first 8 `alignments`).
3. For each hit, use `Entrez.efetch` (db=`'protein'`, rettype=`'fasta'`, retmode=`'text'`) to download the protein sequence. Build a `SeqRecord` list.
4. Write the sequences to `data/blast_top8.faa` with `SeqIO.write`.
5. Run **ClustalW** on `data/blast_top8.faa`; read the alignment and guide tree.
6. Run **MUSCLE** on the same file (FASTA output); read the alignment and guide tree.

   **Note:** MUSCLE does not produce a `.dnd` file by default. To get a Newick tree from MUSCLE, build it from the alignment using `Bio.Phylo.TreeConstruction`:
   ```python
   from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
   calculator = DistanceCalculator('identity')
   dm = calculator.get_distance(align_muscle)
   constructor = DistanceTreeConstructor()
   tree_muscle = constructor.nj(dm)
   ```

7. Draw **both trees side-by-side** in a single matplotlib figure with two subplots.
8. Save the figure to `~/Images/phylo_comparison.pdf`.

**Hint:** pass `axes=ax` to `Phylo.draw(tree, axes=ax)` to draw into a specific subplot axis.

### Solution

<details>
<summary>Show solution</summary>

```python
from pathlib import Path
from Bio import SeqIO, Entrez, AlignIO, Phylo
from Bio.Blast import NCBIXML
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio.Align.Applications import ClustalwCommandline, MuscleCommandline
from Bio.Phylo.TreeConstruction import (
    DistanceCalculator, DistanceTreeConstructor)
import matplotlib.pyplot as plt

Entrez.email = 'nome@esempio.it'
IMGDIR = Path.home() / 'Images'

# ── 1. Parse BLAST output ──────────────────────────────────
with open('data/blastOutput_DRR076693.3.xml', 'r') as f:
    blast_record = NCBIXML.read(f)

top8 = blast_record.alignments[:8]

# ── 2-3. Fetch protein sequences ──────────────────────────
seq_records = []
for hit in top8:
    h = Entrez.efetch(
        db='protein', id=hit.accession,
        rettype='fasta', retmode='text')
    fetched = list(SeqIO.parse(h, 'fasta'))
    if fetched:
        seq_records.append(fetched[0])

# ── 4. Write FASTA ────────────────────────────────────────
SeqIO.write(seq_records, 'data/blast_top8.faa', 'fasta')
print(f'Written {len(seq_records)} sequences to data/blast_top8.faa')

# ── 5. ClustalW ──────────────────────────────────────────
cline = ClustalwCommandline(
    'clustalw2', infile='data/blast_top8.faa')
cline()

align_clustal = AlignIO.read('data/blast_top8.aln', 'clustal')
tree_clustal  = Phylo.read('data/blast_top8.dnd', 'newick')
tree_clustal.rooted = True

# ── 6. MUSCLE + tree construction ────────────────────────
muscle_cline = MuscleCommandline(
    'muscle',
    input='data/blast_top8.faa',
    out='data/blast_top8_muscle.afa')
muscle_cline()

align_muscle = AlignIO.read('data/blast_top8_muscle.afa', 'fasta')

calculator   = DistanceCalculator('identity')
dm           = calculator.get_distance(align_muscle)
constructor  = DistanceTreeConstructor()
tree_muscle  = constructor.nj(dm)
tree_muscle.rooted = True

# ── 7-8. Side-by-side plot ───────────────────────────────
plt.style.use('lecturesOliveFluo')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.set_title('ClustalW', fontsize=13)
Phylo.draw(tree_clustal, axes=ax1, do_show=False)

ax2.set_title('MUSCLE + NJ', fontsize=13)
Phylo.draw(tree_muscle, axes=ax2, do_show=False)

fig.tight_layout()
fig.savefig(IMGDIR / 'phylo_comparison.pdf', bbox_inches='tight')
print('Saved to', IMGDIR / 'phylo_comparison.pdf')
```

</details>
