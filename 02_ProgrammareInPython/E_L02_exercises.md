# Exercises — Python Basics

**Covered lectures:** L02_a (Intro & Environment), L02_b (Source Code), L02_c (Variables),
L02_d (Instructions & Operators), L02_e (Expressions), L02_f (Variables Advanced),
L02_g (Selection), L02_h (While Loop)

---

## Exercise 1 — Your first biological variable (difficulty: ★)

A DNA sequence is just a string of characters. Store the following sequence in a variable,
then print its length, its type, and the character at position 7 (0-indexed).

```
ATGCGTACGATCGATCGTA
```

**Expected output:**
```
Sequence: ATGCGTACGATCGATCGTA
Length: 19
Type: <class 'str'>
Base at position 7: A
```

> **Hint:** Use `len()`, `type()`, and string indexing `s[i]`.

### Solution

<details>
<summary>Show solution</summary>

```python
sequence = "ATGCGTACGATCGATCGTA"

print("Sequence:", sequence)
print("Length:", len(sequence))
print("Type:", type(sequence))
print("Base at position 7:", sequence[7])
```

</details>

---

## Exercise 2 — GC content (difficulty: ★★)

The GC content of a DNA sequence is the fraction of bases that are either G or C.
It is commonly used as a measure of sequence composition and stability.

Given the sequence below, compute and print the GC content as a percentage rounded to 2 decimal places.

```
ATGCGTACGATCGATCGTAGCCATG
```

**Expected output:**
```
G count: 7
C count: 6
GC content: 52.0%
```

> **Hint:** Use the string method `.count()`. Pay attention to operator precedence when
> computing the fraction: `(G + C) / total * 100`.

### Solution

<details>
<summary>Show solution</summary>

```python
sequence = "ATGCGTACGATCGATCGTAGCCATG"

g_count = sequence.count("G")
c_count = sequence.count("C")
gc_content = (g_count + c_count) / len(sequence) * 100

print("G count:", g_count)
print("C count:", c_count)
print(f"GC content: {gc_content:.2f}%")
```

**Why precedence matters:** `g_count + c_count / len(sequence) * 100` would divide `c_count`
by `len(sequence)` first (left-to-right), giving a wrong result. Always use parentheses.

</details>

---
## Exercise 3 — Sequence validator and classifier (difficulty: ★★★)

Write a program that:

1. Asks the user to enter a DNA sequence (uppercase).
2. Checks whether the sequence contains only valid DNA bases (`A`, `T`, `G`, `C`).
   If not, print `"Invalid sequence"` and stop.
3. If valid, classifies the GC content:
   - GC < 40% → `"AT-rich"`
   - 40% ≤ GC ≤ 60% → `"Balanced"`
   - GC > 60% → `"GC-rich"`
4. Also classifies each base as purine (`A`, `G`) or pyrimidine (`C`, `T`) and prints the counts.

**Example run:**
```
Enter a DNA sequence: ATGCGTACGATCG
GC content: 53.85%
Classification: Balanced
Purines (A/G): 8
Pyrimidines (C/T): 5
```

> **Hint:** Build a string of valid bases `"ATGC"` and check each character with `in`.
> Use `if/elif/else` for classification.

### Solution

<details>
<summary>Show solution</summary>

```python
sequence = input("Enter a DNA sequence: ").upper()

valid_bases = "ATGC"
for base in sequence:
    if base not in valid_bases:
        print("Invalid sequence")
        exit()

gc_content = (sequence.count("G") + sequence.count("C")) / len(sequence) * 100
print(f"GC content: {gc_content:.2f}%")

if gc_content < 40:
    print("Classification: AT-rich")
elif gc_content <= 60:
    print("Classification: Balanced")
else:
    print("Classification: GC-rich")

purines = sequence.count("A") + sequence.count("G")
pyrimidines = sequence.count("C") + sequence.count("T")
print("Purines (A/G):", purines)
print("Pyrimidines (C/T):", pyrimidines)
```

</details>

---

## Exercise 4 — Finding the first stop codon (difficulty: ★★★★)

A stop codon signals the end of a protein-coding region. The three DNA stop codons are:
`TAA`, `TAG`, and `TGA`.

Write a program that:

1. Takes the sequence below and scans it **codon by codon** (every 3 bases from position 0)
   using a **while loop**.
2. Prints each codon and its position.
3. Stops and reports when it finds the first stop codon (or reports "No stop codon found"
   if the loop completes without finding one).

```
ATGAAACGTAGTTTACGATAA
```

**Expected output:**
```
Position 0: ATG
Position 3: AAA
Position 6: CGT
Position 9: AGT
Position 12: TTA
Position 15: CGA
Position 18: TAA — STOP codon found!
```

> **Hint:** Use `i = 0` and advance by 3 each iteration. Extract the codon with `sequence[i:i+3]`.
> Make sure the loop condition also handles the case where the remaining bases are fewer than 3.

### Solution

<details>
<summary>Show solution</summary>

```python
sequence = "ATGAAACGTAGTTTACGATAA"
stop_codons = {"TAA", "TAG", "TGA"}

i = 0
stop_found = False

while i + 3 <= len(sequence) and not stop_found:
    codon = sequence[i:i+3]
    if codon in stop_codons:
        print(f"Position {i}: {codon} — STOP codon found!")
        stop_found = True
    else:
        print(f"Position {i}: {codon}")
        i += 3

if not stop_found:
    print("No stop codon found")
```

**Note:** The termination condition is expressed entirely in the `while` predicate:
the loop exits either because the sequence is exhausted (`i + 3 > len(sequence)`) or
because a stop codon was found (`stop_found`). Using a `set` for `stop_codons` makes
membership testing (`in`) efficient — a good habit even when the set is small.

</details>
