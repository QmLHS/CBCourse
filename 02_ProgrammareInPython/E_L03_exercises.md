# Exercises — Data Structures and Functions

**Covered lectures:** L03_a (Data Structures Intro), L03_b (Strings), L03_c (Tuples),
L03_d (Lists), L03_e (Dictionaries), L03_f (Loops & Iterators),
L03_g (Multidimensional), L03_h (Functions), L03_i (Functions Advanced)

---

## Exercise 1 — Reverse complement (difficulty: ★)

In molecular biology, the reverse complement of a DNA strand is the sequence you would
read on the complementary strand in the 5'→3' direction. To compute it:

1. Replace each base with its complement: `A↔T`, `G↔C`.
2. Reverse the resulting string.

Write a function `reverse_complement(seq)` that takes a DNA sequence and returns its
reverse complement. Test it on the sequence `ATGCGTACG`.

**Expected output:**
```
Original:           ATGCGTACG
Reverse complement: CGTACGCAT
```

> **Hint:** Build the complement base by base using a dictionary `{"A": "T", "T": "A", ...}`,
> accumulate characters into a string with `+`, then reverse with slicing `[::-1]`.

### Solution

<details>
<summary>Show solution</summary>

```python
def reverse_complement(seq):
    complement = {"A": "T", "T": "A", "G": "C", "C": "G"}
    comp_seq = ""
    for base in seq:
        comp_seq = comp_seq + complement[base]
    return comp_seq[::-1]

sequence = "ATGCGTACG"
rc = reverse_complement(sequence)
print("Original:          ", sequence)
print("Reverse complement:", rc)
```

</details>

---

## Exercise 2 — Genomic intervals (difficulty: ★★)

Genomic features (genes, exons, regulatory regions) are represented as intervals
`(start, end)` on a chromosome. Use **tuples** and **lists** to answer the questions below.

You are given a dictionary mapping gene names to their `(start, end)` coordinates on
the same chromosome:

```python
genes = {
    "geneA": (100,  400),
    "geneB": (250,  600),
    "geneC": (700,  900),
    "geneD": (1000, 1500),
    "geneE": (380,  420),
}
```

Write code that:

1. Prints the length (in base pairs) of each gene.
2. Builds a new list containing only the names of genes longer than 200 bp.
3. Finds and prints all pairs of genes that **overlap** (i.e., their intervals share at
   least one position). Two intervals `(s1, e1)` and `(s2, e2)` overlap if `s1 < e2` and `s2 < e1`.

**Expected output:**
```
geneA: 300 bp
geneB: 350 bp
geneC: 200 bp
geneD: 500 bp
geneE: 40 bp

Genes longer than 200 bp: ['geneA', 'geneB', 'geneD']

Overlapping pairs:
  geneA and geneB overlap
  geneA and geneE overlap
  geneB and geneE overlap
```

> **Hint:** Iterate with `.items()` to unpack name and coordinates together.
> For the overlap check, convert `genes.keys()` to a list so you can index it,
> then use a nested loop starting the inner index at `i + 1` to avoid duplicate pairs.

### Solution

<details>
<summary>Show solution</summary>

```python
genes = {
    "geneA": (100,  400),
    "geneB": (250,  600),
    "geneC": (700,  900),
    "geneD": (1000, 1500),
    "geneE": (380,  420),
}

# 1. Print gene lengths
for name, (start, end) in genes.items():
    print(f"{name}: {end - start} bp")

# 2. Genes longer than 200 bp
long_genes = []
for name, (start, end) in genes.items():
    if end - start > 200:
        long_genes.append(name)
print("\nGenes longer than 200 bp:", long_genes)

# 3. Overlapping pairs
print("\nOverlapping pairs:")
names = list(genes.keys())
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        name1, name2 = names[i], names[j]
        s1, e1 = genes[name1]
        s2, e2 = genes[name2]
        if s1 < e2 and s2 < e1:
            print(f"  {name1} and {name2} overlap")
```

</details>

---

## Exercise 3 — Codon usage table (difficulty: ★★★)

Codon usage bias — the unequal use of synonymous codons — varies across organisms and
affects translation efficiency. Build a codon frequency dictionary from a coding sequence.

Given the sequence below (assume it starts at position 0 and has no partial codons):

```
ATGAAACGTAGTTTACGATAAATGCGTCGT
```

Write code that:

1. Splits the sequence into codons and stores their counts in a dictionary.
2. Prints the contents of the frequency dictionary.
3. Identifies and prints the most frequent codon and the stop codon (if present).

**Expected output:**
```
Codon frequencies:
  ATG: 2
  AAA: 1
  CGT: 3
  AGT: 1
  TTA: 1
  CGA: 1
  TAA: 1

Most frequent codon: CGT (3 times)
Stop codon found: TAA
```

> **Hint:** Use `dict.get(key, 0) + 1` to count without `KeyError`.
> To find the most frequent codon, iterate over the dictionary keeping track of the
> maximum count seen so far.

### Solution

<details>
<summary>Show solution</summary>

```python
sequence = "ATGAAACGTAGTTTACGATAAATGCGTCGT"
stop_codons = {"TAA", "TAG", "TGA"}

codon_freq = {}
for i in range(0, len(sequence) - 2, 3):
    codon = sequence[i:i+3]
    codon_freq[codon] = codon_freq.get(codon, 0) + 1

print("Codon frequencies:")
for codon, count in codon_freq.items():
    print(f"  {codon}: {count}")

max_count = 0
most_frequent_codon = ""
for codon, count in codon_freq.items():
    if count > max_count:
        max_count = count
        most_frequent_codon = codon
print(f"\nMost frequent codon: {most_frequent_codon} ({max_count} times)")

found_stop = ""
for codon in codon_freq:
    if codon in stop_codons:
        found_stop = codon
if found_stop != "":
    print("Stop codon found:", found_stop)
else:
    print("No stop codon found")
```

</details>

---

## Exercise 4 — Dot matrix and translation pipeline (difficulty: ★★★★)

This exercise combines multidimensional data structures and functions to build two
classic bioinformatics tools.

### Part A — Dot matrix

A dot matrix is a way to visualize similarity between two sequences: place a `1` in
cell `(i, j)` if `seq1[i] == seq2[j]`, otherwise `0`.

Write a function `dot_matrix(seq1, seq2)` that returns a 2D list (list of lists)
representing the dot matrix, and a function `print_dot_matrix(matrix, seq1, seq2)`
that prints it in a readable format using `.` for 0 and `*` for 1.

Test with:
```python
seq1 = "ATGCAT"
seq2 = "TGCATG"
```

**Expected output:**
```
    T G C A T G
A [ . . . * . . ]
T [ * . . . * . ]
G [ . * . . . * ]
C [ . . * . . . ]
A [ . . . * . . ]
T [ * . . . * . ]
```

### Part B — Translation function

Write a function `translate(seq, reading_frame=0)` that:
- Starts at `reading_frame` (0, 1, or 2)
- Translates codons until it hits a stop codon or runs out of sequence
- Returns the amino acid sequence as a string

Use the minimal codon table below (standard genetic code, 20 amino acids + stop):

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
```

Test with `seq = "ATGAAACGTAGTTTACGATAA"` and all three reading frames.

**Expected output:**
```
Frame 0: MKR SLR* → MKR
Frame 1: *
Frame 2: ETVSLD
```

> **Hint for Part B:** Use `reading_frame` as the starting index. Use a `while` loop whose
> condition checks both that there are still at least 3 bases left **and** that the last
> decoded amino acid was not `"*"`. Use `.get(codon, "?")` to handle unknown codons.

### Solution

<details>
<summary>Show solution</summary>

```python
# Part A
def dot_matrix(seq1, seq2):
    matrix = []
    for i in range(len(seq1)):
        row = []
        for j in range(len(seq2)):
            if seq1[i] == seq2[j]:
                row.append(1)
            else:
                row.append(0)
        matrix.append(row)
    return matrix

def print_dot_matrix(matrix, seq1, seq2):
    header = "    " + " ".join(seq2)
    print(header)
    for i in range(len(matrix)):
        cells = []
        for v in matrix[i]:
            if v == 1:
                cells.append("*")
            else:
                cells.append(".")
        print(f"{seq1[i]} [ {' '.join(cells)} ]")

seq1 = "ATGCAT"
seq2 = "TGCATG"
matrix = dot_matrix(seq1, seq2)
print_dot_matrix(matrix, seq1, seq2)

# Part B
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

seq = "ATGAAACGTAGTTTACGATAA"
for frame in range(3):
    protein = translate(seq, reading_frame=frame)
    print(f"Frame {frame}: {protein if protein else '(empty)'}")
```

</details>
