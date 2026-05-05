# Exercises — File I/O and Capstone

**Covered lectures:** L04_a (File I/O), L04_c (Exercises)

These exercises assume you are comfortable with all concepts from the L02 and L03 sessions.
They focus on reading and writing files and on building complete, end-to-end programs.

---

## Exercise 1 — Reading a FASTA file (difficulty: ★)

FASTA is the most common plain-text format for biological sequences. Each entry consists
of a header line starting with `>` followed by a sequence identifier and optional
description, then one or more lines of sequence data.

Example file (`sequences.fasta`):
```
>seq1 Homo sapiens BRCA1 exon 11 fragment
ATGCGTACGATCGATCGTAGCCATGAAACGTAGTTTACGATAA
>seq2 Mus musculus Trp53 fragment
ATGCGTAAAGCTAGCTAGCATGCGTCGT
>seq3 Arabidopsis thaliana RuBisCO fragment
GCTAGCTAGCATGCGTATCGATCGATCGATCGATCGATCG
```

Create this file manually (or use `sce288c.fasta` from the parent folder if available).

Write a Python script that:

1. Opens the FASTA file and reads it line by line.
2. For each sequence entry, prints the sequence ID (first word after `>`) and the
   total length of the sequence.

**Expected output:**
```
seq1 — 43 bp
seq2 — 28 bp
seq3 — 40 bp
```

> **Hint:** Use `open(filename)` and a `for line in f:` loop. Strip whitespace with `.strip()`.
> Track whether you are inside a sequence or at a header by checking `line.startswith(">")`.

### Solution

<details>
<summary>Show solution</summary>

```python
filename = "sequences.fasta"

current_id = None
current_seq = []

with open(filename) as f:
    for line in f:
        line = line.strip()
        if line.startswith(">"):
            if current_id is not None:
                print(f"{current_id} — {len(current_seq)} bp")
            current_id = line[1:].split()[0]
            current_seq = []
        else:
            current_seq.extend(list(line))

if current_id is not None:
    print(f"{current_id} — {len(current_seq)} bp")
```

**Key pattern:** accumulate sequence lines, flush when you hit the next `>` header.
The final sequence needs to be printed after the loop ends.

</details>

---

## Exercise 2 — Parsing a gene expression table (difficulty: ★★)

Gene expression experiments produce tables with gene identifiers and expression values
across conditions. A common format is a tab-separated values (TSV) file.

Create a file called `expression.tsv` with this content:

```
gene_id	condition_A	condition_B
BRCA1	12.4	8.1
TP53	45.2	50.3
EGFR	3.1	2.9
MYC	102.5	88.7
PTEN	7.8	6.2
RB1	0.5	0.3
KRAS	33.0	41.2
```

Write a script that:

1. Reads the file, skipping the header line.
2. Stores the data in a dictionary: `{gene_id: (condition_A, condition_B)}`.
3. Filters and prints only genes where the expression in **either** condition exceeds
   a threshold entered by the user.
4. For each selected gene, also prints the fold change: `condition_B / condition_A`
   rounded to 2 decimal places.

**Example run (threshold = 10):**
```
Expression threshold: 10
BRCA1   A=12.40  B=8.10   FC=0.65
TP53    A=45.20  B=50.30  FC=1.11
MYC     A=102.50 B=88.70  FC=0.87
KRAS    A=33.00  B=41.20  FC=1.25
```

> **Hint:** Use `float()` to convert the values read from the file. `str.split("\t")` or
> `str.split()` splits on whitespace/tabs.

### Solution

<details>
<summary>Show solution</summary>

```python
filename = "expression.tsv"
threshold = float(input("Expression threshold: "))

expression = {}
with open(filename) as f:
    next(f)  # skip header
    for line in f:
        parts = line.strip().split("\t")
        gene_id = parts[0]
        cond_a = float(parts[1])
        cond_b = float(parts[2])
        expression[gene_id] = (cond_a, cond_b)

for gene, (a, b) in expression.items():
    if a > threshold or b > threshold:
        fc = b / a
        print(f"{gene:<8} A={a:<8.2f} B={b:<8.2f} FC={fc:.2f}")
```

</details>

---

## Exercise 3 — Filtering sequences and writing output (difficulty: ★★★)

You will now combine reading and writing files to build a filtering pipeline — a very
common task in bioinformatics workflows.

Using the `sequences.fasta` file from Exercise 1 (or any multi-sequence FASTA file):

Write a script that:

1. Asks the user for a minimum GC content threshold (e.g., `40`).
2. Reads all sequences from the FASTA file.
3. Computes the GC content of each sequence.
4. Writes sequences that **pass** the threshold to `filtered.fasta`, preserving the
   original header lines.
5. Prints a summary to the screen.

**Example run:**
```
Minimum GC content (%): 50
--- Filtering results ---
seq1 (GC=46.51%) → EXCLUDED
seq2 (GC=57.14%) → INCLUDED
seq3 (GC=56.41%) → INCLUDED

2 / 3 sequences written to filtered.fasta
```

> **Hint:** Build a list of `(header, sequence)` tuples while reading, then iterate
> over the list to filter and write. Use `"w"` mode for the output file.

### Solution

<details>
<summary>Show solution</summary>

```python
input_file = "sequences.fasta"
output_file = "filtered.fasta"
threshold = float(input("Minimum GC content (%): "))

# Read all sequences
sequences = []
current_header = None
current_seq = []

with open(input_file) as f:
    for line in f:
        line = line.strip()
        if line.startswith(">"):
            if current_header is not None:
                sequences.append((current_header, "".join(current_seq)))
            current_header = line
            current_seq = []
        else:
            current_seq.append(line)
    if current_header is not None:
        sequences.append((current_header, "".join(current_seq)))

# Filter and write
passed = 0
print("--- Filtering results ---")

with open(output_file, "w") as out:
    for header, seq in sequences:
        seq_id = header[1:].split()[0]
        gc = (seq.count("G") + seq.count("C")) / len(seq) * 100
        if gc >= threshold:
            out.write(header + "\n")
            out.write(seq + "\n")
            passed += 1
            status = "INCLUDED"
        else:
            status = "EXCLUDED"
        print(f"{seq_id} (GC={gc:.2f}%) → {status}")

print(f"\n{passed} / {len(sequences)} sequences written to {output_file}")
```

</details>

---

## Exercise 4 — Full sequence analysis pipeline (difficulty: ★★★★)

Build a complete, reusable analysis pipeline that integrates all concepts from this session.

### Scenario

You have a FASTA file with multiple coding sequences. You want to:

1. Parse the file and build a dictionary `{seq_id: sequence}`.
2. For each sequence, compute:
   - Length (bp)
   - GC content (%)
   - Number of stop codons in reading frame 0
   - Predicted protein sequence (reading frame 0, stop at first stop codon)
3. Write a summary TSV file (`summary.tsv`) with columns:
   `seq_id`, `length`, `gc_content`, `stop_codons_rf0`, `protein_rf0`
4. Write a FASTA file (`proteins.fasta`) with the translated protein sequences.
5. Print how many sequences have a valid start codon (`ATG` at position 0).

Use `sequences.fasta` from Exercise 1, or create a richer test file:

```
>orf1
ATGAAACGTAGTTTACGATAA
>orf2
ATGGCCATCGAATGA
>orf3
GCTAGCTAGCATGCGTATCGA
>orf4
ATGCGTCGTATGAAATAA
```

> **Hint:** Organise your code into functions: `parse_fasta(filename)`,
> `gc_content(seq)`, `count_stops(seq)`, `translate(seq)`. This mirrors the
> refactoring you saw in `indovinaLaParolaFunzione.py`.

### Solution

<details>
<summary>Show solution</summary>

```python
CODON_TABLE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}

def parse_fasta(filename):
    sequences = {}
    current_id = None
    current_seq = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_id:
                    sequences[current_id] = "".join(current_seq)
                current_id = line[1:].split()[0]
                current_seq = []
            else:
                current_seq.append(line)
    if current_id:
        sequences[current_id] = "".join(current_seq)
    return sequences

def gc_content(seq):
    return (seq.count("G") + seq.count("C")) / len(seq) * 100

def count_stops(seq):
    stop_codons = {"TAA", "TAG", "TGA"}
    count = 0
    for i in range(0, len(seq) - 2, 3):
        if seq[i:i+3] in stop_codons:
            count = count + 1
    return count

def translate(seq, reading_frame=0):
    protein = []
    i = reading_frame
    aa = ""
    while i + 3 <= len(seq) and aa != "*":
        aa = CODON_TABLE.get(seq[i:i+3], "?")
        if aa != "*":
            protein.append(aa)
        i += 3
    return "".join(protein)


sequences = parse_fasta("sequences.fasta")

with open("summary.tsv", "w") as tsv, open("proteins.fasta", "w") as prot_out:
    tsv.write("seq_id\tlength\tgc_content\tstop_codons_rf0\tprotein_rf0\n")
    for seq_id, seq in sequences.items():
        gc = gc_content(seq)
        stops = count_stops(seq)
        protein = translate(seq)
        tsv.write(f"{seq_id}\t{len(seq)}\t{gc:.2f}\t{stops}\t{protein}\n")
        prot_out.write(f">{seq_id}\n{protein}\n")

has_start = 0
for seq in sequences.values():
    if seq.startswith("ATG"):
        has_start = has_start + 1
print(f"Sequences with start codon (ATG): {has_start} / {len(sequences)}")
print("Summary written to summary.tsv")
print("Proteins written to proteins.fasta")
```

</details>
