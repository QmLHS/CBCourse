# Exercises — Git and GitHub

**Covered lectures:** L07_setup (GitHub Account & SSH), L07_a Part 1 (Local Git),
L07_a Part 2 (GitHub), L07_a Part 3 (Collaborative Git)

**Prerequisites:** A GitHub account and a working SSH key (see L07_setup).

---

## Exercise 1 — Your first repository (difficulty: ★)

### Scenario

You are starting a research project on DNA sequence composition.
You will track your notes and findings with Git from day one.

### Tasks

1. Create a new folder called `dna_notes` and initialise a Git repository inside it.

2. Create a file called `README.md` with the following content:
   ```
   # DNA Composition Notes
   A collection of notes on nucleotide composition in biological sequences.
   ```
   Stage and commit it with the message `"Add project README"`.

3. Create a second file called `gc_content.md` with these contents:
   ```
   ## GC Content

   GC content is the percentage of G and C bases in a DNA sequence.
   High GC content generally correlates with higher melting temperature.

   ### Example
   Sequence: ATGCGTACGATCG
   G count: 4
   C count: 3
   GC content: 53.8%
   ```
   Stage and commit it with an appropriate message.

4. Make a small edit to `README.md` (add one sentence of your choice).
   Before staging, run `git diff` to see the change.
   Then stage and commit it.

5. Run `git log --oneline` and verify you have exactly 3 commits.

**Expected final state:**
```
$ git log --oneline
c4f1a2b Update README with project description
7e3d901 Add GC content notes
a1b2c3d Add project README
```

> **Hint:** The sequence of commands for each step is:
> `git status` → `git add <file>` → `git status` → `git commit -m "..."`

### Solution

<details>
<summary>Show solution</summary>

```bash
mkdir dna_notes
cd dna_notes
git init
git config user.name "Your Name"
git config user.email "you@example.com"

# Step 2
cat > README.md << 'EOF'
# DNA Composition Notes
A collection of notes on nucleotide composition in biological sequences.
EOF
git add README.md
git commit -m "Add project README"

# Step 3
cat > gc_content.md << 'EOF'
## GC Content

GC content is the percentage of G and C bases in a DNA sequence.
High GC content generally correlates with higher melting temperature.

### Example
Sequence: ATGCGTACGATCG
G count: 4
C count: 3
GC content: 53.8%
EOF
git add gc_content.md
git commit -m "Add GC content notes"

# Step 4
echo "Sequences with GC > 60% are considered GC-rich." >> README.md
git diff
git add README.md
git commit -m "Update README with project description"

# Step 5
git log --oneline
```

</details>

---

## Exercise 2 — History and recovery (difficulty: ★★)

### Scenario

You introduce an error into your notes and need to inspect the history
and recover a previous state.

### Tasks

Continue working in the `dna_notes` repository from Exercise 1.

1. Open `gc_content.md` and delete the entire `### Example` section
   (the last 5 lines). Save the file.

2. Before staging, use `git diff` to review exactly what you deleted.

3. You realise this was a mistake. Use the appropriate Git command to
   **discard the unstaged change** and restore the file to its last
   committed state.

4. Verify the file is back to its original content, then run `git status`
   to confirm the working directory is clean.

5. Now intentionally stage the deletion (`git add gc_content.md`) and
   then change your mind. Use `git restore --staged` to unstage it,
   then `git restore` to discard it entirely.

6. Add a new section to `gc_content.md`:
   ```
   ### AT-rich sequences
   Sequences with GC < 40% are called AT-rich.
   They are common in non-coding intergenic regions.
   ```
   Commit this addition.

7. Use `git log --oneline` and then `git show <hash>` on your most recent
   commit to see exactly what was added.

> **Hint:** `git restore <file>` discards unstaged changes.
> `git restore --staged <file>` moves changes back from staging to working directory.

### Solution

<details>
<summary>Show solution</summary>

```bash
# Step 1 — edit gc_content.md and remove the Example section
# (use a text editor or VS Code)

# Step 2
git diff

# Step 3 — discard the change
git restore gc_content.md

# Step 4
cat gc_content.md
git status

# Step 5
git add gc_content.md
git status
git restore --staged gc_content.md
git status
git restore gc_content.md
git status

# Step 6
cat >> gc_content.md << 'EOF'

### AT-rich sequences
Sequences with GC < 40% are called AT-rich.
They are common in non-coding intergenic regions.
EOF
git add gc_content.md
git commit -m "Add AT-rich sequence section to GC content notes"

# Step 7
git log --oneline
git show HEAD    # HEAD always refers to the most recent commit
```

</details>

---

## Exercise 3 — Pushing to GitHub (difficulty: ★★★)

### Scenario

Your notes are ready to be shared. You will publish the repository
to GitHub and practise the push/pull cycle.

### Prerequisites

A working GitHub account and SSH key (see L07_setup).

### Tasks

1. On GitHub, create a new **empty** public repository called `dna_notes`.
   Do not add a README, .gitignore, or licence — leave everything unchecked.

2. Back in your local `dna_notes` folder, connect the local repo to GitHub:
   ```bash
   git remote add origin git@github.com:<your_username>/dna_notes.git
   ```
   Verify with `git remote -v`.

3. Push your local history to GitHub:
   ```bash
   git push -u origin main
   ```
   Open the repository in your browser and confirm you can see all your
   commits and files.

4. On the GitHub web interface, click on `README.md` → the pencil icon
   to edit it online. Add a line:
   ```
   Maintained by: <your name>
   ```
   Scroll down and commit directly to `main` with an appropriate message.

5. Back in your terminal, run `git pull` to fetch that remote change.
   Confirm that `README.md` now contains the line you added online.

6. Make one more local change (add a new file `codons.md` with a brief
   note about codons), commit it, and push it with `git push`.

> **Hint:** After step 3, the `-u` flag means future `git push` and
> `git pull` will automatically target `origin main` — you do not need
> to type the full command again.

### Solution

<details>
<summary>Show solution</summary>

```bash
# Step 2
git remote add origin git@github.com:<your_username>/dna_notes.git
git remote -v

# Step 3
git push -u origin main

# Steps 4–5 are done on the GitHub web interface, then:
git pull
cat README.md

# Step 6
cat > codons.md << 'EOF'
## Codons

A codon is a triplet of nucleotides that encodes one amino acid.
There are 64 possible codons: 61 encode amino acids, 3 are stop codons.
EOF
git add codons.md
git commit -m "Add codon notes"
git push
```

</details>

---

## Exercise 4 — Branching and collaboration (difficulty: ★★★★)

### Scenario

You will now add a Python analysis script to the project.
Following good practice, you will develop it on a dedicated branch
and merge it back once it is complete.

### Tasks

1. From `main`, create and switch to a new branch called `feature/gc-script`.

2. Create a file called `gc_analysis.py` with the following starter code
   and commit it with the message `"Add GC analysis script skeleton"`:

   ```python
   def gc_content(seq):
       pass

   def classify_gc(gc):
       pass

   seq = input("Enter a DNA sequence: ").upper()
   gc = gc_content(seq)
   print(f"GC content: {gc:.2f}%")
   print("Classification:", classify_gc(gc))
   ```

3. Implement `gc_content(seq)`: it should return the GC percentage
   (a float between 0 and 100).
   Commit the implementation with the message `"Implement gc_content function"`.

4. Implement `classify_gc(gc)`: it should return `"AT-rich"` if `gc < 40`,
   `"Balanced"` if `40 <= gc <= 60`, and `"GC-rich"` otherwise.
   Commit the implementation with the message `"Implement gc classification"`.

5. Switch back to `main` and merge the branch:
   ```bash
   git checkout main
   git merge feature/gc-script
   ```
   Confirm the merge with `git log --oneline` — all branch commits should
   now appear on `main`.

6. Push the updated `main` to GitHub and delete the feature branch
   locally (it has been merged, it is no longer needed):
   ```bash
   git branch -d feature/gc-script
   ```

### Bonus — Simulate a Conflict

If you are working with a partner:

1. Both partners clone the repository.
2. Partner A edits the first line of `gc_analysis.py` on `main` and pushes.
3. Partner B (without pulling first) also edits the first line differently and tries to push.
4. Partner B's push will be rejected. They must `git pull` first, resolve
   the conflict manually in the file, then commit and push.

> **Hint:** The full sequence for the merge conflict resolution is:
> `git pull` → edit the file to remove `<<<<`, `====`, `>>>>` markers →
> `git add gc_analysis.py` → `git commit`.

### Solution

<details>
<summary>Show solution</summary>

```bash
# Step 1
git checkout -b feature/gc-script

# Step 2
cat > gc_analysis.py << 'EOF'
def gc_content(seq):
    pass

def classify_gc(gc):
    pass

seq = input("Enter a DNA sequence: ").upper()
gc = gc_content(seq)
print(f"GC content: {gc:.2f}%")
print("Classification:", classify_gc(gc))
EOF
git add gc_analysis.py
git commit -m "Add GC analysis script skeleton"

# Step 3 — implement gc_content
# Edit gc_analysis.py: replace the body of gc_content with:
#
#   g_count = seq.count("G")
#   c_count = seq.count("C")
#   return (g_count + c_count) / len(seq) * 100
#
git add gc_analysis.py
git commit -m "Implement gc_content function"

# Step 4 — implement classify_gc
# Edit gc_analysis.py: replace the body of classify_gc with:
#
#   if gc < 40:
#       return "AT-rich"
#   elif gc <= 60:
#       return "Balanced"
#   else:
#       return "GC-rich"
#
git add gc_analysis.py
git commit -m "Implement gc classification"

# Step 5
git checkout main
git merge feature/gc-script
git log --oneline

# Step 6
git push
git branch -d feature/gc-script
```

</details>
