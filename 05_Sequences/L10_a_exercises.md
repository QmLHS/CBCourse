# Exercises — Biological Sequences: FASTA Parsing

**Covered lecture:** L10_a

**Datasets** (inside `05_Sequences/data/`):

| File | Notes |
|------|-------|
| `opuntia.fasta` | 7 nucleotide sequences from *Opuntia* (cactus), each ~500 bp; NCBI FASTA headers (`gi|num|gb|acc|locus`) |
| `codonTable.txt` | Tab-separated file, columns `codon\taminoacid`, 64 entries (one per codon) |

---

## Exercise 1 — Loading a FASTA file with BioPython (difficulty: ★)

### Scenario
You have received a multi-FASTA file containing several sequences from the cactus genus *Opuntia*. Before any analysis you need a quick inventory: how many sequences are in the file and what are their lengths?

### Tasks
1. Use `SeqIO.parse` from `Bio` to load `data/opuntia.fasta`.
2. Print the **total number of sequences** in the file.
3. For each sequence, print its **ID** and **length** (in bp).

### Expected output (format)
```
Total sequences: 7
gi|6273291|gb|AF191665.1|AF191665    499 bp
gi|6273290|gb|AF191664.1|AF191664    ??? bp
...
```

### Hints
- `SeqIO.parse` returns an iterator; use a counter or `len(list(...))`.
- The length of a sequence is `len(seq_record.seq)`.

### Solution
<details>
<summary>Show solution</summary>

```python
from Bio import SeqIO

records = list(SeqIO.parse('data/opuntia.fasta', 'fasta'))

print(f"Total sequences: {len(records)}")
for rec in records:
    print(f"{rec.id:<45} {len(rec.seq)} bp")
```
</details>

---

## Exercise 2 — Dictionary access and GC content (difficulty: ★★)

### Scenario
You want to access a specific sequence by its identifier and compute its GC content — a basic quality indicator and useful feature in comparative genomics.

### Tasks
1. Use `SeqIO.to_dict` to build a dictionary from `data/opuntia.fasta`.
2. Access sequence `'gi|6273291|gb|AF191665.1|AF191665'` directly by key.
3. Print the **first 50** and **last 50** bases of that sequence.
4. Compute and print the **GC content** as a percentage (fraction of G+C bases over total length).

### Expected output (format)
```
First 50 bp: TATACATTAAAGAAGGGGGATGCGGATAAATGGAAAGGCGAAAGAAAGAA
Last  50 bp: ...
GC content:  41.28%
```

### Hints
- GC content = `(seq.count('G') + seq.count('C')) / len(seq) * 100`
- Consider converting `seq` to uppercase first (`.upper()`).

### Solution
<details>
<summary>Show solution</summary>

```python
from Bio import SeqIO

dict_seqs = SeqIO.to_dict(SeqIO.parse('data/opuntia.fasta', 'fasta'))

target_id = 'gi|6273291|gb|AF191665.1|AF191665'
rec = dict_seqs[target_id]
seq = str(rec.seq).upper()

print(f"First 50 bp: {seq[:50]}")
print(f"Last  50 bp: {seq[-50:]}")

gc = (seq.count('G') + seq.count('C')) / len(seq) * 100
print(f"GC content:  {gc:.2f}%")
```
</details>

---

## Exercise 3 — Manual FASTA parser and the EOF bug (difficulty: ★★)

### Scenario
Understanding how parsers work under the hood is essential for debugging and for handling non-standard files. You will implement a naive FASTA parser, observe its main flaw, and then fix it.

### Tasks
1. Implement a function `parse_fasta_naive(filename)` that reads `data/opuntia.fasta` line by line (without BioPython) and returns a dict:
   ```python
   { gi_number: {'gi': ..., 'emb': ..., 'locus': ..., 'seq': ...} }
   ```
   Use `|` as the separator in the defline, extracting `tokens[1]` (gi), `tokens[3]` (emb/accession), `tokens[4]` (locus).
2. Call the function and print **how many records** it returns. Notice the bug: the last record is missing.
3. Fix the function so that all 7 records are returned. (Hint: after the loop, check whether there is an unsaved record.)

### Expected output
```
Naive parser: 6 records  ← bug: last record lost
Fixed parser: 7 records
```

### Solution
<details>
<summary>Show solution</summary>

```python
def parse_fasta_naive(filename):
    """Naive FASTA parser — loses the last record."""
    diz_seqs = {}
    diz_seq = None
    sequence = ''
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == '>':
                tokens = line[1:].strip().split('|')
                diz_seq = {
                    'gi':    tokens[1],
                    'emb':   tokens[3],
                    'locus': tokens[4].strip()
                }
                sequence = ''
            elif line[0] in ['\r', '\n']:
                diz_seq['seq'] = sequence
                diz_seqs[diz_seq['gi']] = diz_seq
            else:
                sequence += line.strip()
    return diz_seqs


def parse_fasta_fixed(filename):
    """Fixed FASTA parser — handles the last record correctly."""
    diz_seqs = {}
    diz_seq = None
    sequence = ''
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == '>':
                # save previous record before starting a new one
                if diz_seq is not None:
                    diz_seq['seq'] = sequence
                    diz_seqs[diz_seq['gi']] = diz_seq
                tokens = line[1:].strip().split('|')
                diz_seq = {
                    'gi':    tokens[1],
                    'emb':   tokens[3],
                    'locus': tokens[4].strip()
                }
                sequence = ''
            else:
                sequence += line.strip()
    # save the very last record
    if diz_seq is not None:
        diz_seq['seq'] = sequence
        diz_seqs[diz_seq['gi']] = diz_seq
    return diz_seqs


naive = parse_fasta_naive('data/opuntia.fasta')
fixed = parse_fasta_fixed('data/opuntia.fasta')

print(f"Naive parser: {len(naive)} records")
print(f"Fixed parser: {len(fixed)} records")
```
</details>

---

## Exercise 4 — All reading frames and stop codons (difficulty: ★★★)

### Scenario
A coding sequence must be read in the correct reading frame. A wrong frame typically produces many premature stop codons. You will explore all three forward reading frames for each *Opuntia* sequence.

### Tasks
1. Load all 7 sequences from `data/opuntia.fasta` using BioPython.
2. For each sequence and each reading frame (`+0`, `+1`, `+2`), translate using `seq[offset:].translate()`.
3. Count the number of **stop codons** (`'*'`) in each translated protein.
4. Print a table: sequence ID, frame, stop count.
5. Compute and print the **average stop count per frame** across all sequences. Which frame has the fewest stop codons on average?

### Expected output (format)
```
ID                                          Frame  Stops
gi|6273291|gb|AF191665.1|AF191665           +0     3
gi|6273291|gb|AF191665.1|AF191665           +1     5
...
Average stops:  +0=3.4   +1=5.1   +2=4.7
Frame with fewest stops on average: +0
```

### Hints
- `str(prot).count('*')` counts stop codons in the translated string.
- Frame `+k` is obtained with `seq[k:].translate()`.

### Solution
<details>
<summary>Show solution</summary>

```python
from Bio import SeqIO

records = list(SeqIO.parse('data/opuntia.fasta', 'fasta'))

results = []  # (id, frame, stop_count)

for rec in records:
    for frame in range(3):
        prot = rec.seq[frame:].translate()
        stops = str(prot).count('*')
        results.append((rec.id, frame, stops))
        print(f"{rec.id:<45}  +{frame}  {stops}")

# average per frame
for frame in range(3):
    avg = sum(s for _, f, s in results if f == frame) / len(records)
    print(f"Average stops +{frame}: {avg:.2f}")

best_frame = min(range(3),
                 key=lambda f: sum(s for _, fr, s in results if fr == f))
print(f"Frame with fewest stops on average: +{best_frame}")
```
</details>

---

## Exercise 5 — Manual translation and comparison with BioPython (difficulty: ★★★★)

### Scenario
Building your own translation function from scratch forces you to understand codon tables, edge cases (sequence length not divisible by 3, unknown codons), and lets you verify whether a third-party library agrees with your implementation.

### Tasks
1. Write a function `translate_naive(dna_seq, codon_table_file)` that:
   - Loads `data/codonTable.txt` (tab-separated: `codon\taminoacid`).
   - Translates `dna_seq` in reading frame `+0` only.
   - Skips the trailing bases if `len(dna_seq) % 3 != 0`.
   - Uses `'?'` for any codon not found in the table.
2. Identify the **longest sequence** in `data/opuntia.fasta`.
3. Apply `translate_naive` to that sequence.
4. Compare the result with BioPython's `seq.translate()`.
5. Are they identical? If not, explain any differences you observe. (Think about: uppercase vs. lowercase input, stop codons, codon table version.)

### Hints
- `max(records, key=lambda r: len(r.seq))` finds the longest record.
- Use `str(seq).upper()` before passing to your function to avoid case issues.
- BioPython's default table is NCBI standard table 1. Your `codonTable.txt` may or may not match exactly — check for stop codons and rare codons.

### Solution
<details>
<summary>Show solution</summary>

```python
from Bio import SeqIO


def load_codon_table(codon_table_file):
    """Load codon -> amino acid mapping from a tab-separated file."""
    table = {}
    with open(codon_table_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 2:
                table[parts[0].upper()] = parts[1]
    return table


def translate_naive(dna_seq, codon_table_file):
    """
    Translate dna_seq in frame +0 using a codon table file.
    Unknown codons are represented as '?'.
    Trailing bases (if len % 3 != 0) are ignored.
    """
    table = load_codon_table(codon_table_file)
    dna = str(dna_seq).upper()
    protein = []
    for i in range(0, len(dna) - len(dna) % 3 - 2, 3):
        codon = dna[i:i+3]
        protein.append(table.get(codon, '?'))
    return ''.join(protein)


# find the longest record
records = list(SeqIO.parse('data/opuntia.fasta', 'fasta'))
longest = max(records, key=lambda r: len(r.seq))
print(f"Longest sequence: {longest.id}  ({len(longest.seq)} bp)")

# manual translation
prot_naive = translate_naive(longest.seq, 'data/codonTable.txt')

# BioPython translation
prot_biopython = str(longest.seq.upper().translate())

print(f"\nManual:    {prot_naive[:40]}...")
print(f"BioPython: {prot_biopython[:40]}...")

if prot_naive == prot_biopython:
    print("\nThe two translations are identical.")
else:
    print("\nThe translations differ.")
    # find first position of disagreement
    for i, (a, b) in enumerate(zip(prot_naive, prot_biopython)):
        if a != b:
            print(f"  First difference at position {i}: "
                  f"naive='{a}', biopython='{b}'")
            break
    if len(prot_naive) != len(prot_biopython):
        print(f"  Length: naive={len(prot_naive)}, "
              f"biopython={len(prot_biopython)}")
    print("\n  Possible reasons: uppercase/lowercase handling,")
    print("  stop codon symbol ('*' vs other), codon table version.")
```
</details>
