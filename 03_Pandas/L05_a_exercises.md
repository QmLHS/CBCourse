# Exercises — Pandas: Reading Data

**Covered lecture:** L05_a

**Datasets** (all inside `03_Pandas/`):

| File | Notes |
|------|-------|
| `RawData/MeteoMilano2011.csv` | Daily weather in Milan 2011, 365 rows, 23 columns |
| `RawData/7-nani.csv` | Seven names, no header |
| `RawData/2009-2013_iscritti.csv` | Italian university enrollments, semicolon-delimited |
| `RawData/2009-2013_gettito_contribuzione.csv` | University funding, semicolon-delimited, European decimals |
| `RawData/2009-2013_strutture.csv` | University structures, with dates |

---

## Exercise 1 — First look (difficulty: ★)

### Scenario

You received a CSV file with daily weather measurements for Milan in 2011.
Before doing any analysis you want to understand the structure of the data.

### Tasks

1. Load `RawData/MeteoMilano2011.csv` into a DataFrame called `meteo`.
2. Print the number of rows and columns.
3. Print all column names.
4. Display the first 5 rows.
5. Display the last 3 rows.

**Expected output (excerpt):**
```
Rows: 365, Columns: 23
First column: CET
Last 3 rows show dates in December 2011.
```

> **Hint:** Use `.shape`, `.columns`, `.head()`, `.tail()`.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

meteo = pd.read_csv("RawData/MeteoMilano2011.csv")

rows, cols = meteo.shape
print(f"Rows: {rows}, Columns: {cols}")
print("Columns:", meteo.columns.tolist())
print(meteo.head(5))
print(meteo.tail(3))
```

</details>

---

## Exercise 2 — Header trouble (difficulty: ★★)

### Scenario

You are given `RawData/7-nani.csv`, a file with no column header.
If you load it without the right parameter, the first name becomes the header — ruining the data.

### Tasks

1. First, load the file **incorrectly** (without `names=`) and observe the problem.
2. Load it correctly with `names=['Name']`.
3. How many entries are in the file?
4. Is the name `"Bashful"` present? Print `True` or `False`.
5. Print the list of names sorted alphabetically.

**Expected output:**
```
Entries: 7
Bashful present: True
Sorted: ['Bashful', 'Doc', 'Dopey', 'Grumpy', 'Happy', 'Sleepy', 'Sneezy']
```

> **Hint:** For step 4, use `'Bashful' in nani['Name'].values`.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

# Step 1 — wrong load
bad = pd.read_csv("RawData/7-nani.csv")
print("Wrong (first name became header):", bad.columns.tolist())

# Step 2 — correct load
nani = pd.read_csv("RawData/7-nani.csv", names=['Name'])

# Step 3
print("Entries:", len(nani))

# Step 4
present = 'Bashful' in nani['Name'].values
print("Bashful present:", present)

# Step 5
print("Sorted:", sorted(nani['Name'].tolist()))
```

</details>

---

## Exercise 3 — Enrollment data (difficulty: ★★)

### Scenario

The Ministry publishes Italian university enrollment data as a semicolon-delimited CSV.
You need to load it correctly and answer a few questions.

### Tasks

1. Load `RawData/2009-2013_iscritti.csv` using the correct separator.
2. Print the shape and the column names.
3. How many unique universities (`COD_ATENEO`) are in the file?
4. How many unique academic years (`ANNO_ACCADEMICO`) are in the file?
5. Filter to rows where `DESCRIZIONE_ISCRIZIONE == 'Totale iscritti'`.
   Which academic year has the highest total value of `ISCRITTI_LAUREA`?

**Expected output (excerpt):**
```
Shape: (720, 9)
Unique universities: 59
Unique years: 5
Year with most Bachelor's students: 2009-2010 (or similar)
```

> **Hint:** For step 5, use `.groupby()` and `.sum()` on the filtered DataFrame, then `.idxmax()`.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

iscritti = pd.read_csv("RawData/2009-2013_iscritti.csv",
                       delimiter=';')

print("Shape:", iscritti.shape)
print("Columns:", iscritti.columns.tolist())
print("Unique universities:", iscritti['COD_ATENEO'].nunique())
print("Unique years:", iscritti['ANNO_ACCADEMICO'].nunique())

totale = iscritti[iscritti['DESCRIZIONE_ISCRIZIONE'] == 'Totale iscritti']
by_year = totale.groupby('ANNO_ACCADEMICO')['ISCRITTI_LAUREA'].sum()
best_year = by_year.idxmax()
print(f"Year with most Bachelor's students: {best_year} ({by_year[best_year]:,})")
```

</details>

---

## Exercise 4 — European format (difficulty: ★★★)

### Scenario

The funding file uses the continental European convention (semicolons, comma decimals).
Loading it without the right parameters will silently break numerical computations.

### Tasks

1. Load `RawData/2009-2013_gettito_contribuzione.csv` **without** `decimal=','`.
   Check the dtype of the `CONSUNTIVO` column — is it numeric?
2. Reload the file **with** the correct `decimal=','` parameter.
   Confirm that `CONSUNTIVO` is now numeric.
3. Compute the **total funding per year** (`ANNO_SOLARE`) across all universities.
4. Which year had the highest total funding?
5. By how many percent did funding change from the first year to the last?

> **Hint:** For step 5, compute `(last - first) / first * 100`.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

# Step 1 — wrong load
bad = pd.read_csv("RawData/2009-2013_gettito_contribuzione.csv",
                  delimiter=';')
print("Wrong dtype:", bad['CONSUNTIVO'].dtype)

# Step 2 — correct load
gettito = pd.read_csv("RawData/2009-2013_gettito_contribuzione.csv",
                      delimiter=';',
                      decimal=',')
print("Correct dtype:", gettito['CONSUNTIVO'].dtype)

# Step 3
by_year = gettito.groupby('ANNO_SOLARE')['CONSUNTIVO'].sum()
print(by_year)

# Step 4
print("Best year:", by_year.idxmax(), f"({by_year.max():,.0f} €)")

# Step 5
years = sorted(by_year.index)
change = (by_year[years[-1]] - by_year[years[0]]) / by_year[years[0]] * 100
print(f"Change from {years[0]} to {years[-1]}: {change:+.1f}%")
```

</details>

---

## Exercise 5 — Structures with dates (difficulty: ★★★)

### Scenario

The structures file contains a date column in Italian day-first format (`DD/MM/YY`).
Your goal is to load it with correct date parsing and extract meaningful information.

### Tasks

1. Load `RawData/2009-2013_strutture.csv` with:
   - the correct separator
   - `DATA` parsed as a datetime, with Italian date order
2. Confirm that `DATA` has dtype `datetime64`.
3. What is the most recent date in the dataset?
4. Filter to rows where `DATA` is in the year 2013.
5. Among the rows from 2013, which university (`NOME_ATENEO`) has the highest total `NUMERO_STRUTTURE`?

> **Hint:** To filter by year, use `df['DATA'].dt.year == 2013`.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

strutture = pd.read_csv(
    "RawData/2009-2013_strutture.csv",
    delimiter=';',
    parse_dates=['DATA'],
    dayfirst=True
)

print("DATA dtype:", strutture['DATA'].dtype)
print("Most recent date:", strutture['DATA'].max())

s2013 = strutture[strutture['DATA'].dt.year == 2013]
by_uni = s2013.groupby('NOME_ATENEO')['NUMERO_STRUTTURE'].sum()
best = by_uni.idxmax()
print(f"University with most structures in 2013: {best} ({by_uni[best]})")
```

</details>
