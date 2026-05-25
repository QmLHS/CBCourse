# Exercises — Biological Sequences: FASTQ and Sequence Quality

**Covered lecture:** L10_b

**Datasets** (inside `05_Sequences/data/`):

| File | Notes |
|------|-------|
| `SRR020192.fastq` | 41,892 Illumina reads in Sanger FASTQ format (offset 33) |
| `DRR076693.fastq` | *S. cerevisiae* RNA-seq reads; use first 500 for analysis |

---

## Exercise 1 — Exploring a FASTQ file (difficulty: ★)

### Scenario
Before any analysis you need a basic characterisation of the dataset: how many reads it contains, their length range, and what the first read looks like.

### Tasks
1. Use `SeqIO.parse` to load `data/SRR020192.fastq`.
2. Print the **total number of reads**.
3. Print the **minimum** and **maximum read length** across all reads.
4. Print the **ID** and the full **sequence** of the first read.

### Expected output (format)
```
Total reads: 41892
Min length:  ?? bp
Max length:  ?? bp
First read ID:  SRR020192.1 HWI-EAS359_7_FC62BK1:1:1:416:946/1
First read seq: GTTTGACAGCAGCTTGGCAGTTGGCTTGTTTTTTC
```

### Hints
- Store all records in a list to be able to iterate twice (once for count/lengths, once for the first record), or capture the first record during a single pass.
- `len(rec.seq)` gives the read length.

### Solution
<details>
<summary>Show solution</summary>

```python
from Bio import SeqIO

records = list(SeqIO.parse('data/SRR020192.fastq', 'fastq'))

print(f"Total reads: {len(records)}")
lengths = [len(r.seq) for r in records]
print(f"Min length:  {min(lengths)} bp")
print(f"Max length:  {max(lengths)} bp")

first = records[0]
print(f"First read ID:  {first.description}")
print(f"First read seq: {first.seq}")
```
</details>

---

## Exercise 2 — Filtering by minimum quality (difficulty: ★★)

### Scenario
Low-quality reads introduce errors in downstream analyses (assembly, variant calling, expression quantification). A common pre-processing step is to discard reads where at least one base has a quality score below a threshold.

### Tasks
1. Filter `data/SRR020192.fastq` keeping only reads where **all** bases have $Q \geq 20$.
2. Save the passing reads to `data/filtered_Q20.fastq`.
3. Print how many reads pass the filter and what fraction of the original file that represents.

### Expected output (format)
```
Reads passing Q>=20 filter: 20050
Fraction retained: 47.86%
```

### Hints
- Use a generator expression with `min(rec.letter_annotations['phred_quality']) >= 20`.
- `SeqIO.write` returns the number of records written.
- Fraction = `count_kept / total * 100`.

### Solution
<details>
<summary>Show solution</summary>

```python
from Bio import SeqIO

total = sum(1 for _ in SeqIO.parse('data/SRR020192.fastq', 'fastq'))

good_reads = (
    rec for rec in SeqIO.parse('data/SRR020192.fastq', 'fastq')
    if min(rec.letter_annotations['phred_quality']) >= 20
)

kept = SeqIO.write(good_reads, 'data/filtered_Q20.fastq', 'fastq')

print(f"Reads passing Q>=20 filter: {kept}")
print(f"Fraction retained: {kept / total * 100:.2f}%")
```
</details>

---

## Exercise 3 — Generator function for primer trimming (difficulty: ★★)

### Scenario
Many sequencing protocols leave a known primer sequence at the start of each read. Before assembly or alignment, the primer must be removed. You will write a reusable generator function that handles both cases (primer present / absent) and preserves the quality scores.

### Tasks
1. Write a generator function `trim_primer(records, primer)` that:
   - yields `record[len(primer):]` if the read starts with the primer
   - yields the record unchanged otherwise
2. Apply it to all reads in `data/SRR020192.fastq` using primer `'GATGACGGTGT'`.
3. Save the output to `data/trimmed.fastq`.
4. Print how many reads were actually trimmed (i.e., had the primer).

### Hints
- `record.seq.startswith(primer)` returns `True`/`False`.
- Slicing a `SeqRecord` (`record[n:]`) trims both the sequence and the quality string simultaneously.
- Keep a counter inside the generator, or make two passes.

### Solution
<details>
<summary>Show solution</summary>

```python
from Bio import SeqIO

PRIMER = 'GATGACGGTGT'
trimmed_count = 0


def trim_primer(records, primer):
    global trimmed_count
    for rec in records:
        if rec.seq.startswith(primer):
            trimmed_count += 1
            yield rec[len(primer):]
        else:
            yield rec


trimmed_reads = trim_primer(
    SeqIO.parse('data/SRR020192.fastq', 'fastq'),
    PRIMER
)
SeqIO.write(trimmed_reads, 'data/trimmed.fastq', 'fastq')

print(f"Reads trimmed (primer found): {trimmed_count}")
```

*Note:* using a global counter inside a generator is a simple approach.
An alternative is to count with a separate pass using `startswith`:

```python
with_primer = sum(
    1 for rec in SeqIO.parse('data/SRR020192.fastq', 'fastq')
    if rec.seq.startswith(PRIMER)
)
print(f"Reads with primer: {with_primer}")  # -> 13819
```
</details>

---

## Exercise 4 — Best quality read with SeqIO.index (difficulty: ★★★)

### Scenario
`SeqIO.index` allows random access to records in a large FASTQ file without loading everything into memory — it reads only the index (byte offsets) and fetches records on demand. This is essential when working with files that are tens of gigabytes.

### Tasks
1. Use `SeqIO.index` to open `data/SRR020192.fastq`.
2. Retrieve the **first 500 read IDs** from the index (use `list(fqDict.keys())[:500]`).
3. For each of those 500 reads, compute the **average Q score** (mean of `phred_quality`).
4. Identify the read with the **highest average Q score** among the 500.
5. Print its **ID**, **sequence**, and **average Q score**.

### Hints
- `fqDict[rid].letter_annotations['phred_quality']` is a list of integers.
- `sum(lst) / len(lst)` computes the mean.
- Use `max(...)` with a key function.

### Solution
<details>
<summary>Show solution</summary>

```python
from Bio import SeqIO

fqDict = SeqIO.index('data/SRR020192.fastq', 'fastq')

ids_500 = list(fqDict.keys())[:500]

def avg_quality(rid):
    phred = fqDict[rid].letter_annotations['phred_quality']
    return sum(phred) / len(phred)

best_id = max(ids_500, key=avg_quality)
best_rec = fqDict[best_id]
best_avg = avg_quality(best_id)

print(f"Best read ID:      {best_id}")
print(f"Sequence:          {best_rec.seq}")
print(f"Average Q score:   {best_avg:.2f}")
```
</details>

---

## Exercise 5 — Per-position quality profile (difficulty: ★★★★)

### Scenario
Visualising quality as a function of read position is the first thing a bioinformatician does when receiving a new dataset. Quality typically degrades towards the end of reads due to signal decay in Illumina sequencing. You will reproduce a plot similar to FastQC's "Per base sequence quality" panel.

### Tasks
1. Load the **first 500 reads** from `data/DRR076693.fastq` using `SeqIO.index`.
2. Build a Pandas DataFrame where **rows are reads** and **columns are base positions**. Each cell contains the Phred quality score at that position (use `pd.Series` and `pd.DataFrame`).
3. Compute per-position **mean** and **IQR** (25th and 75th percentile).
4. Plot a quality profile (up to position 300 or the maximum read length, whichever is shorter):
   - Mean Q score as a dot/line plot
   - IQR as a shaded band (`fill_between`)
   - Coloured background: red for $Q < 20$, yellow for $20 \leq Q < 28$, green for $Q \geq 28$
5. Label both axes and add a legend.

### Hints
- Reads of different lengths produce `NaN` in missing columns; `dfFQ.mean()` ignores `NaN` by default.
- Use `dfFQ.quantile([0.25, 0.75])` to get the IQR bounds.
- `ax.fill_between(range(nBases), lower, upper, alpha=0.3)` draws the IQR band.

### Solution
<details>
<summary>Show solution</summary>

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Bio import SeqIO
from pathlib import Path

plt.style.use('lecturesOliveFluo')

IMGDIR = Path.home() / 'Images'

# load first 500 reads
fqDict = SeqIO.index('data/DRR076693.fastq', 'fastq')
ids = list(fqDict.keys())[:500]

rows = [
    pd.Series(fqDict[rid].letter_annotations['phred_quality'],
              name=rid)
    for rid in ids
]
dfFQ = pd.DataFrame(rows)

# per-position statistics
mean = dfFQ.mean()
q    = dfFQ.quantile([0.25, 0.75])

nBases = min(300, dfFQ.shape[1])

fig, ax = plt.subplots(figsize=(12, 4))

# coloured quality zones
ax.fill_between(range(nBases),  0, 20,
                color='red',    alpha=0.15, label='Q < 20')
ax.fill_between(range(nBases), 20, 28,
                color='yellow', alpha=0.15, label='Q 20–28')
ax.fill_between(range(nBases), 28, 43,
                color='green',  alpha=0.15, label='Q ≥ 28')

# IQR band
ax.fill_between(range(nBases),
                q.iloc[0, :nBases],
                q.iloc[1, :nBases],
                alpha=0.35, label='IQR (25–75%)')

# mean line
ax.plot(mean[:nBases], '.', markersize=3, label='Mean Q')

ax.set_xlim(0, nBases - 1)
ax.set_ylim(0, 43)
ax.set_xlabel('Base position (bp)')
ax.set_ylabel('Phred Q score')
ax.set_title('Per-position quality profile — DRR076693 (first 500 reads)')
ax.legend(fontsize=8, loc='lower left')

fig.tight_layout()
fig.savefig(IMGDIR / 'fastq_quality_profile.pdf', bbox_inches='tight')
plt.show()
```
</details>
