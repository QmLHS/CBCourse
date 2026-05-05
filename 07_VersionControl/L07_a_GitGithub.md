---
title: "Git and GitHub"
subtitle: "Version Control for Computational Research"
author: "Dario Pescini"
institute: |
  Università degli Studi di Milano-Bicocca \newline
  Dipartimento di Statistica e Metodi Quantitativi
date: ""
---

# Part 1 — Local Version Control

## The Problem

Have you ever found yourself doing this?

```
analysis.py
analysis_v2.py
analysis_v2_final.py
analysis_v2_final_FIXED.py
analysis_v2_final_FIXED_actually_final.py
```

\vspace{0.3cm}
Questions that become impossible to answer:

- What changed between these versions?
- Which one produced the results in my report?
- Can I recover the version from two weeks ago?


## Version Control Solves This

A **version control system** (VCS) records the full history
of a project, file by file, change by change.

\vspace{0.3cm}
\begin{columns}
\begin{column}{0.5\textwidth}
\textbf{Without VCS}
\begin{itemize}
  \item Multiple copies of files
  \item No record of what changed or why
  \item Hard to collaborate
  \item Recovery depends on luck
\end{itemize}
\end{column}
\begin{column}{0.5\textwidth}
\textbf{With Git}
\begin{itemize}
  \item One copy, full history
  \item Every change is explained
  \item Collaboration with conflicts resolved explicitly
  \item Any past state is recoverable
\end{itemize}
\end{column}
\end{columns}


## Git — The Key Concepts

```
 Working directory      Staging area        Repository
 ─────────────────      ────────────        ──────────
  your files as          files ready         permanent
  you edit them   ──▶    to snapshot  ──▶    snapshots
                git add              git commit
```

\vspace{0.4cm}

| Term | Meaning |
|------|---------|
| **repository** | a folder whose history Git tracks |
| **commit** | a named snapshot of the staging area |
| **staging area** | where you choose what goes into the next commit |


## First-Time Configuration

Run once on every machine you use:

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
git config --global core.editor "code --wait"
git config --global init.defaultBranch main
```

\vspace{0.3cm}
Check your settings:

```bash
git config --list
```


## Starting a Repository

```bash
mkdir genome_analysis
cd genome_analysis
git init
```

\vspace{0.2cm}
Git creates a hidden `.git/` folder — the repository database.
Never edit it manually.

\vspace{0.3cm}
```bash
git status          # always safe to run — shows current state
```

Output:
```
On branch main
No commits yet
nothing to commit
```


## Your First Commit

```bash
# create a file
echo "# GC Content Analysis" > notes.md

git status          # notes.md appears as "untracked"

git add notes.md    # move to staging area
git status          # now "Changes to be committed"

git commit -m "Add initial analysis notes"
```

\vspace{0.3cm}
The commit message is addressed to your future self —
write *why*, not just *what*.


## The Staging Area — Why Does It Exist?

It lets you build a focused, meaningful commit even when
several files have changed:

```bash
# You edited three files:
#   gc_content.py   ← new feature
#   notes.md        ← documentation update
#   scratch.py      ← unfinished experiment

git add gc_content.py
git add notes.md
git commit -m "Implement GC content function and document it"

# scratch.py is left out — it will go in a later commit
```


## Viewing History

```bash
git log                 # full log with author, date, message
git log --oneline       # compact: one commit per line
git log --oneline -5    # last 5 commits only
```

\vspace{0.3cm}
Example output:
```
a3f2e1c Add GC content function
8b91d04 Add initial analysis notes
```

Each commit has a unique **hash** (the hexadecimal code) — this
is how you refer to any past state.


## Inspecting Changes

```bash
git diff                    # unstaged changes vs last commit
git diff --staged           # staged changes vs last commit
git show a3f2e1c            # what a specific commit changed
```

\vspace{0.3cm}
Output format — lines starting with:

| Symbol | Meaning |
|--------|---------|
| `+` | added |
| `-` | removed |
| (none) | unchanged context |


## Undoing Changes

```bash
# Discard unstaged changes in a file (cannot be recovered!)
git restore notes.md

# Unstage a file (keep the changes, just remove from staging)
git restore --staged notes.md

# Look at (but not change) the state at a past commit
git checkout a3f2e1c
git checkout main           # return to the present
```

\vspace{0.3cm}
> `git restore` is safe — it only touches unstaged or staged files.
> `git checkout <hash>` puts you in "detached HEAD" state — read only.


## What to Track — and What Not to

**Track:**

- Source code, scripts, notebooks
- Documentation, markdown notes
- Configuration files

\vspace{0.2cm}
**Do not track:**

- Large data files (use a data store or DVC)
- Generated outputs (PDFs, plots, compiled binaries)
- Secrets (passwords, API keys)

\vspace{0.3cm}
Use a `.gitignore` file to exclude patterns:

```
*.pdf
__pycache__/
.env
data/raw/
```


# Part 2 — GitHub

## What Is GitHub?

GitHub is a **hosting platform for Git repositories**.

\vspace{0.3cm}
\begin{columns}
\begin{column}{0.5\textwidth}
\textbf{What it adds to Git}
\begin{itemize}
  \item Remote backup
  \item Web interface to browse history
  \item Pull requests and code review
  \item Issue tracking
  \item CI/CD integration
\end{itemize}
\end{column}
\begin{column}{0.5\textwidth}
\textbf{Alternatives}
\begin{itemize}
  \item GitLab (self-hostable)
  \item Bitbucket
  \item Codeberg (open source)
\end{itemize}
\end{column}
\end{columns}

\vspace{0.3cm}
Git is the tool. GitHub is one place to store the result.


## Creating a Remote Repository

1. Go to **github.com** → click **+** → *New repository*
2. Name it (e.g. `genome_analysis`)
3. Choose **Public** or **Private**
4. **Leave all checkboxes empty** — you already have a local repo

\vspace{0.3cm}
GitHub will show you a set of commands — we will use the
*"push an existing repository"* option.


## Connecting Local to Remote

```bash
# Tell your local repo where the remote is
git remote add origin git@github.com:youruser/genome_analysis.git

# Verify
git remote -v
```

\vspace{0.3cm}
Output:
```
origin  git@github.com:youruser/genome_analysis.git (fetch)
origin  git@github.com:youruser/genome_analysis.git (push)
```

`origin` is just the conventional name for the main remote.


## Pushing and Pulling

```bash
# First push: -u sets origin/main as the tracking branch
git push -u origin main

# Subsequent pushes (after new commits)
git push

# Fetch remote changes and merge into your local branch
git pull
```

\vspace{0.3cm}
The typical daily workflow:

```
git pull        ← start the day: get others' changes
... edit ...
git add
git commit
git push        ← end the day: share your changes
```


## Cloning an Existing Repository

To get a copy of any repository (yours or someone else's):

```bash
git clone git@github.com:youruser/genome_analysis.git

# Or clone to a custom folder name
git clone git@github.com:youruser/genome_analysis.git my_local_copy
```

\vspace{0.3cm}
`git clone` does everything in one step:

- Creates the folder
- Initialises a git repo
- Downloads the full history
- Sets up `origin` automatically


## Remote + Local — The Full Picture

```
GitHub (remote)
  origin/main  ─────────────────────────────────┐
                                                 │
                    git push                     │
              ─────────────────▶                 │
Your machine                                     │
  local main   ◀─────────────────                │
                    git pull                     │
                                                 │
  Working dir  ──▶  Staging  ──▶  Local repo  ──┘
               git add        git commit
```


# Part 3 — Collaborative Git

## Why Branches?

On a shared project, committing directly to `main` causes problems:

- Half-finished work breaks others' code
- Two people editing the same file at the same time → conflict
- Hard to review changes before they reach the stable version

\vspace{0.3cm}
**Branches** let each person (or each feature) have an isolated
line of development that only merges into `main` when it is ready.


## Working with Branches

```bash
git branch                      # list all branches
git checkout -b feature/gc-plot # create and switch to new branch
git switch main                 # return to main (modern syntax)
git branch -d feature/gc-plot   # delete a merged branch
```

\vspace{0.3cm}
Convention: name branches after what they do.

```
main                    ← stable, always works
feature/gc-plot         ← new feature in progress
fix/parser-crash        ← bug fix
experiment/new-model    ← exploratory, may be discarded
```


## The Branch Lifecycle

```
main     ──●──────────────────────────●──▶
            \                        /
             ●────●────●────●────●──   feature/gc-plot
              create   commits       merge
```

\vspace{0.3cm}
```bash
# On feature/gc-plot: develop, commit as usual
git add plot_gc.py
git commit -m "Add GC content plot function"

# When ready, merge back into main
git checkout main
git merge feature/gc-plot
```


## Pull Requests

A **Pull Request (PR)** is a GitHub-level concept:
a formal request to merge one branch into another,
with a built-in review interface.

\vspace{0.3cm}
**Workflow:**

1. Push your branch to GitHub: `git push -u origin feature/gc-plot`
2. GitHub shows a *"Compare & pull request"* button — click it
3. Write a description of your changes
4. Assign reviewers
5. Reviewers comment, request changes, or approve
6. Merge via GitHub interface


## Why PRs Matter for Research

\begin{columns}
\begin{column}{0.5\textwidth}
\textbf{Code review}
\begin{itemize}
  \item Catch bugs before they affect results
  \item Share knowledge across the team
  \item Enforce consistent style
\end{itemize}
\end{column}
\begin{column}{0.5\textwidth}
\textbf{Documentation}
\begin{itemize}
  \item Every change has a reason recorded
  \item Reviewers' comments preserved
  \item Reproducibility: you know exactly what version produced a figure
\end{itemize}
\end{column}
\end{columns}


## Merge Conflicts

A conflict happens when two branches edited **the same lines**
of the same file.

\vspace{0.3cm}
Git marks the conflict in the file:

```
<<<<<<< HEAD
gc = (seq.count("G") + seq.count("C")) / len(seq)
=======
gc = sum(1 for b in seq if b in "GC") / len(seq)
>>>>>>> feature/gc-refactor
```

\vspace{0.2cm}

**Resolution steps:**

1. Open the file, decide which version to keep (or combine them)
2. Remove all `<<<<`, `====`, `>>>>` markers
3. `git add` the resolved file
4. `git commit`


## Forking

A **fork** is a personal copy of someone else's repository on GitHub.

\vspace{0.3cm}
Use it when you want to contribute to a project you do not have
write access to:

1. Fork the repo on GitHub (click *Fork*)
2. Clone **your fork** locally
3. Make changes, push to your fork
4. Open a PR from your fork to the original repo

\vspace{0.3cm}
This is how open-source contributions work — including contributions
to bioinformatics tools like Biopython, Snakemake, or GATK.


## The Standard Collaborative Workflow

```
         fork / clone
              │
              ▼
     git checkout -b feature/xxx
              │
        edit and commit
              │
     git push origin feature/xxx
              │
     open Pull Request on GitHub
              │
      review and discussion
              │
        merge into main
              │
     git pull (update your local main)
```


# Summary

## Commands Reference — Local

| Command | What it does |
|---------|-------------|
| `git init` | Create a new repository |
| `git status` | Show current state |
| `git add <file>` | Stage changes |
| `git commit -m "..."` | Save a snapshot |
| `git log --oneline` | Show history |
| `git diff` | Show unstaged changes |
| `git restore <file>` | Discard unstaged changes |


## Commands Reference — Remote and Branches

| Command | What it does |
|---------|-------------|
| `git remote add origin <url>` | Connect to a remote |
| `git push` | Upload commits to remote |
| `git pull` | Download and merge remote commits |
| `git clone <url>` | Copy a remote repository locally |
| `git checkout -b <name>` | Create and switch to a branch |
| `git merge <branch>` | Merge a branch into the current one |


## Key Takeaways

- **Commit early and often** — small commits are easier to review and revert
- **Write meaningful commit messages** — "fix bug" tells you nothing in six months
- **Never commit secrets** — API keys, passwords; use `.gitignore`
- **Pull before you push** — avoid unnecessary conflicts
- **Use branches for anything non-trivial** — keep `main` always working
- **Git history is your lab notebook** — treat it with the same care
