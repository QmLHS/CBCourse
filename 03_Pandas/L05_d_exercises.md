# Exercises — Pandas: Combining DataFrames

**Covered lecture:** L05_d

**Datasets** (all inside `03_Pandas/`):

| File | Notes |
|------|-------|
| `RawData/MeteoMilano2011.csv` … `MeteoMilano2015.csv` | Five years of daily weather data |
| `RawData/2009-2013_iscritti.csv` | University enrollments, semicolon-delimited |
| `RawData/2009-2013_gettito_contribuzione.csv` | University funding, semicolon + European decimals |
| `RawData/2009-2013_strutture.csv` | University structures with dates |

---

## Exercise 1 — Stacking annual files (difficulty: ★★)

### Scenario

Weather data is stored in separate annual files.
You need to combine them and verify the result.

### Tasks

1. Load `MeteoMilano2011.csv` and `MeteoMilano2012.csv` into two separate DataFrames.
2. Concatenate them with `pd.concat`.  What is the shape of the result?
3. The resulting index has duplicate values (0..364 twice).
   Concatenate again with `ignore_index=True` to get a clean 0-based index.
   Verify the new index with `.index`.
4. Compute the mean of `Temperatura mediaC` for each year separately,
   then for the combined dataset.  Are the values different?  Why?

**Expected output (excerpt):**
```
Combined shape: (730, 23)
2011 mean temp: ...
2012 mean temp: ...
Combined mean temp: ... (average of the two, if balanced)
```

> **Hint:** For step 4, use `df['Temperatura mediaC'].mean()` on each DataFrame
> before combining and on the result after.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

m11 = pd.read_csv("RawData/MeteoMilano2011.csv")
m12 = pd.read_csv("RawData/MeteoMilano2012.csv")

combined = pd.concat([m11, m12])
print("Shape:", combined.shape)
print("Index duplicates?", combined.index.duplicated().any())

combined = pd.concat([m11, m12], ignore_index=True)
print("Clean index:", combined.index)

col = 'Temperatura mediaC'
print(f"2011 mean: {m11[col].mean():.2f}")
print(f"2012 mean: {m12[col].mean():.2f}")
print(f"Combined mean: {combined[col].mean():.2f}")
```

</details>

---

## Exercise 2 — Hierarchical concatenation (difficulty: ★★)

### Scenario

You want to concatenate all five MeteoMilano files and retain which year each row belongs to,
even though the CSV files themselves do not contain a year column.

### Tasks

1. Load all five files (2011--2015) using a dictionary comprehension.
2. Concatenate them with `pd.concat` using the dictionary.
   The result should have a hierarchical (MultiIndex) index.
3. Verify the shape of the result (`5 × 365 rows ≈ 1826`).
4. Access only the 2014 data using `.loc[2014]` on the MultiIndex.
   How many rows does it have?
5. Compute the mean temperature (`Temperatura mediaC`) for each year
   and display the warmest and coldest year.

> **Hint:** After step 2, use `.groupby(level=0)` to group by the outer
> level of the MultiIndex.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

years  = range(2011, 2016)
frames = {y: pd.read_csv(f"RawData/MeteoMilano{y}.csv")
          for y in years}

meteo = pd.concat(frames)
print("Shape:", meteo.shape)
print("Index type:", type(meteo.index))

data_2014 = meteo.loc[2014]
print("2014 rows:", len(data_2014))

col = 'Temperatura mediaC'
mean_by_year = meteo.groupby(level=0)[col].mean()
print(mean_by_year)
print("Warmest year:", mean_by_year.idxmax())
print("Coldest year:", mean_by_year.idxmin())
```

</details>

---

## Exercise 3 — Merging enrollment and funding (difficulty: ★★★)

### Scenario

You want to compare how much each university charges per student on average.
Funding is in one file, enrollment in another, linked by university code.

### Tasks

1. Load both files with the correct parameters (semicolons; European decimals for `gettito`).
2. Notice that the university code column is named `COD_Ateneo` in `gettito`
   and `COD_ATENEO` in `iscritti`.  Use `left_on`/`right_on` to merge on these.
3. Before merging, filter `iscritti` to rows where `DESCRIZIONE_ISCRIZIONE == 'Totale iscritti'`.
4. Aggregate both tables to one row per university per year (use `groupby` + `sum` or `mean`).
5. Merge the aggregated tables, compute `eur_per_student = CONSUNTIVO / iscritti_total`,
   and identify the university with the highest and lowest ratio.

> **Hint:** For the total students, sum `ISCRITTI_LAUREA + ISCRITTI_DOTTORATO +
> ISCRITTI_SPECIALIZZAZIONE + ISCRITTI_MASTER_PERFEZIONAMENTO` before grouping.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

gettito = pd.read_csv("RawData/2009-2013_gettito_contribuzione.csv",
                      delimiter=';', decimal=',')
iscritti = pd.read_csv("RawData/2009-2013_iscritti.csv",
                       delimiter=';')

# Step 3 — filter to totals only
iscritti_tot = iscritti[
    iscritti['DESCRIZIONE_ISCRIZIONE'] == 'Totale iscritti'
].copy()
iscritti_tot['students'] = (
    iscritti_tot['ISCRITTI_LAUREA'] +
    iscritti_tot['ISCRITTI_DOTTORATO'] +
    iscritti_tot['ISCRITTI_SPECIALIZZAZIONE'] +
    iscritti_tot['ISCRITTI_MASTER_PERFEZIONAMENTO']
)

# Step 4 — average over years
gettito_mean   = gettito.groupby('COD_Ateneo', as_index=False)['CONSUNTIVO'].mean()
iscritti_mean  = iscritti_tot.groupby('COD_ATENEO', as_index=False)['students'].mean()

# Step 5
merged = pd.merge(gettito_mean, iscritti_mean,
                  left_on='COD_Ateneo', right_on='COD_ATENEO',
                  validate='1:1')
merged['eur_per_student'] = merged['CONSUNTIVO'] / merged['students']

print("Highest:", merged.loc[merged['eur_per_student'].idxmax(), ['COD_Ateneo', 'eur_per_student']])
print("Lowest:",  merged.loc[merged['eur_per_student'].idxmin(), ['COD_Ateneo', 'eur_per_student']])
```

</details>

---

## Exercise 4 — Diagnosing a merge with indicator (difficulty: ★★★)

### Scenario

Not every university appears in both the funding and the enrollment files.
You need to find out which ones are missing from each side.

### Tasks

1. Load and prepare both files as in Exercise 3 (no need to aggregate here —
   just get the unique university codes from each file).
2. Perform an **outer** merge of the two code lists, adding `indicator=True`.
3. From the `_merge` column, count:
   - how many universities appear in both files
   - how many appear only in `gettito`
   - how many appear only in `iscritti`
4. Print the university names (`NOME_ATENEO`) of the ones that appear only in `gettito`.
5. Use `validate='1:1'` to confirm there are no duplicate codes in either list.

> **Hint:** Get unique codes with `.drop_duplicates()` on `[['COD_Ateneo','NOME_ATENEO']]`.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

gettito  = pd.read_csv("RawData/2009-2013_gettito_contribuzione.csv",
                       delimiter=';', decimal=',')
iscritti = pd.read_csv("RawData/2009-2013_iscritti.csv", delimiter=';')

# Unique codes + names
gettito_uni  = gettito[['COD_Ateneo','NOME_ATENEO']].drop_duplicates()
iscritti_uni = iscritti[['COD_ATENEO','NOME_ATENEO']].drop_duplicates()

# Outer merge with indicator
merged = pd.merge(
    gettito_uni, iscritti_uni,
    left_on='COD_Ateneo', right_on='COD_ATENEO',
    how='outer',
    indicator=True,
    validate='1:1'
)

print(merged['_merge'].value_counts())

only_gettito = merged[merged['_merge'] == 'left_only']
print("Only in gettito:")
print(only_gettito[['COD_Ateneo','NOME_ATENEO_x']].to_string(index=False))
```

</details>

---

## Exercise 5 — Full pipeline (difficulty: ★★★★)

### Scenario

You want to build a ranked table of Italian universities that combines funding,
enrollment, and institution name, and then identify which universities
get the most and least public tuition revenue per student.

### Tasks

1. Load `gettito`, `iscritti`, and `strutture`.
2. From `strutture`, extract a lookup table of unique `(COD_Ateneo, NOME_ATENEO)` pairs
   with no duplicate codes.  If duplicates exist, keep the first name per code.
3. Aggregate `gettito` and `iscritti` to one row per university (5-year mean),
   as in Exercise 3.
4. Merge `gettito_mean` and `iscritti_mean` on the university code (1:1, inner join).
5. Merge the result with the name lookup table to add university names.
6. Compute `eur_per_student` and produce a ranked table (highest to lowest).
   Print the top 5 and bottom 5 universities.

> **Hint:** For step 2, `strutture` has `COD_Ateneo` as a column with a semicolon delimiter.
> Use `.groupby('COD_Ateneo').first()` to get one name per code, then `.reset_index()`.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

gettito  = pd.read_csv("RawData/2009-2013_gettito_contribuzione.csv",
                       delimiter=';', decimal=',')
iscritti = pd.read_csv("RawData/2009-2013_iscritti.csv", delimiter=';')
strutture = pd.read_csv("RawData/2009-2013_strutture.csv",
                        delimiter=';',
                        parse_dates=['DATA'], dayfirst=True)

# Step 2 — unique name lookup
names = (strutture.groupby('COD_Ateneo')['NOME_ATENEO']
                  .first()
                  .reset_index())

# Step 3 — aggregate
iscritti_tot = iscritti[
    iscritti['DESCRIZIONE_ISCRIZIONE'] == 'Totale iscritti'
].copy()
iscritti_tot['students'] = (
    iscritti_tot['ISCRITTI_LAUREA'] +
    iscritti_tot['ISCRITTI_DOTTORATO'] +
    iscritti_tot['ISCRITTI_SPECIALIZZAZIONE'] +
    iscritti_tot['ISCRITTI_MASTER_PERFEZIONAMENTO']
)
gettito_mean  = gettito.groupby('COD_Ateneo', as_index=False)['CONSUNTIVO'].mean()
iscritti_mean = iscritti_tot.groupby('COD_ATENEO', as_index=False)['students'].mean()

# Step 4 — merge funding and enrollment
result = pd.merge(gettito_mean, iscritti_mean,
                  left_on='COD_Ateneo', right_on='COD_ATENEO',
                  how='inner', validate='1:1')

# Step 5 — add names
result = pd.merge(result, names,
                  on='COD_Ateneo',
                  how='left')

# Step 6 — rank
result['eur_per_student'] = result['CONSUNTIVO'] / result['students']
ranked = result[['NOME_ATENEO','eur_per_student']].sort_values(
    'eur_per_student', ascending=False
)
print("Top 5:")
print(ranked.head(5).to_string(index=False))
print("\nBottom 5:")
print(ranked.tail(5).to_string(index=False))
```

</details>
