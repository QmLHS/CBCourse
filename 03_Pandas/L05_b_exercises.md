# Exercises — Pandas: DataFrames and Series

**Covered lecture:** L05_b

**Dataset:** `RawData/incidenti.csv` — Milan traffic incidents 2001--2016 (1920 rows, 6 columns:
`Zona`, `Incidenti`, `Anno`, `Morti`, `Mese`, `Feriti`).
`Zona` has 192 missing values; all other columns are complete.

---

## Exercise 1 — Exploring the structure (difficulty: ★)

### Tasks

1. Load `RawData/incidenti.csv` into a DataFrame called `inc`.
2. Print:
   - the number of rows and columns
   - all column names
   - the data type of each column
3. Show the first 5 rows and the last 3 rows.
4. How many non-missing values does `Zona` have?

**Expected output (excerpt):**
```
Shape: (1920, 6)
Zona non-null count: 1728
```

> **Hint:** Use `.info()` or `.isnull().sum()` to count missing values.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

inc = pd.read_csv("RawData/incidenti.csv")

print("Shape:", inc.shape)
print("Columns:", inc.columns.tolist())
print(inc.dtypes)
print(inc.head(5))
print(inc.tail(3))
print("Zona non-null:", inc['Zona'].count())
```

</details>

---

## Exercise 2 — Column operations (difficulty: ★★)

### Scenario

You want to compute a combined measure of harm per incident record.

### Tasks

1. Extract the `Feriti` column as a Series and print its mean.
2. Create a new column `total_harm` defined as `Morti + Feriti`.
3. Create a new column `severity_index` defined as `(Morti * 3 + Feriti) / Incidenti`.
4. What are the minimum, maximum, and mean values of `severity_index`?
5. Print the 5 rows with the highest `severity_index`.

> **Hint:** Use `.nlargest(5, 'severity_index')` for step 5.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

inc = pd.read_csv("RawData/incidenti.csv")

# Step 1
feriti = inc['Feriti']
print("Mean Feriti:", feriti.mean())

# Steps 2 and 3
inc['total_harm']      = inc['Morti'] + inc['Feriti']
inc['severity_index']  = (inc['Morti'] * 3 + inc['Feriti']) / inc['Incidenti']

# Step 4
print("severity_index — min:", inc['severity_index'].min(),
      "max:", inc['severity_index'].max(),
      "mean:", inc['severity_index'].mean())

# Step 5
print(inc.nlargest(5, 'severity_index')[['Anno', 'Mese', 'Zona', 'severity_index']])
```

</details>

---

## Exercise 3 — iloc and loc (difficulty: ★★)

### Scenario

You need to extract specific subsets of the data using both position-based and label-based indexing.

### Tasks

1. Use `.iloc` to extract rows 10 through 19 (inclusive), keeping only the first 3 columns.
2. Use `.iloc` to extract the last row and print it as a Series.
3. Use `.loc` to extract rows with labels 100 through 110 and the columns `'Anno'` through `'Mese'`.
4. Confirm that `.iloc[100:111]` and `.loc[100:110]` return the same rows
   (compare with `.equals()`).

> **Hint:** Remember that `.iloc` slices exclude the upper bound; `.loc` slices include it.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

inc = pd.read_csv("RawData/incidenti.csv")

# Step 1 — position-based, rows 10-19, first 3 columns
subset_iloc = inc.iloc[10:20, :3]
print(subset_iloc)

# Step 2 — last row
print(inc.iloc[-1])

# Step 3 — label-based, rows 100-110, columns Anno through Mese
subset_loc = inc.loc[100:110, 'Anno':'Mese']
print(subset_loc)

# Step 4 — verify they agree on row content
same_rows_iloc = inc.iloc[100:111]
same_rows_loc  = inc.loc[100:110]
print("Same rows?", same_rows_iloc.equals(same_rows_loc))
```

</details>

---

## Exercise 4 — Boolean filtering (difficulty: ★★★)

### Scenario

An urban planner wants to identify the most critical accident records to prioritise intervention.

### Tasks

1. Filter to rows where `Incidenti > 150`.  How many are there?
2. Filter to rows where `Zona` is either 3 or 4 **and** `Anno >= 2010`.
3. Filter to rows where there were deaths (`Morti > 0`) **but** fewer than 10 injuries (`Feriti < 10`).
   This would indicate unusually severe accidents.  How many such records exist?
4. For the rows from step 3, print the `Anno`, `Mese`, and `Zona` of each.

> **Hint:** Use `&` and `|` and wrap each condition in parentheses.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

inc = pd.read_csv("RawData/incidenti.csv")

# Step 1
high_inc = inc[inc['Incidenti'] > 150]
print("Rows with >150 incidents:", len(high_inc))

# Step 2
zone_3_4 = inc[(inc['Zona'].isin([3, 4])) & (inc['Anno'] >= 2010)]
print("Zone 3 or 4 after 2010:", len(zone_3_4))

# Step 3
severe = inc[(inc['Morti'] > 0) & (inc['Feriti'] < 10)]
print("Deaths with <10 injuries:", len(severe))

# Step 4
print(severe[['Anno', 'Mese', 'Zona']].to_string())
```

</details>

---

## Exercise 5 — Index management (difficulty: ★★★)

### Scenario

You want to reorganise the DataFrame so that `Anno` is the row index,
enabling fast retrieval of all records from a given year.

### Tasks

1. Load the dataset and set `'Anno'` as the index.
2. Use `.loc[2005]` to retrieve all rows from 2005.  How many are there?
3. Compute the total number of incidents in 2005.
4. Reset the index so `Anno` becomes a regular column again.
5. Verify that after resetting, the integer index runs from 0 to 1919.

**Expected output (excerpt):**
```
Rows in 2005: 108
Total incidents in 2005: 10843
Index after reset: RangeIndex(start=0, stop=1920, step=1)
```

> **Hint:** After `set_index`, multiple rows can share the same label — `.loc[2005]` returns all of them.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

inc = pd.read_csv("RawData/incidenti.csv")

# Step 1
inc_idx = inc.set_index('Anno')

# Step 2
rows_2005 = inc_idx.loc[2005]
print("Rows in 2005:", len(rows_2005))

# Step 3
print("Total incidents 2005:", rows_2005['Incidenti'].sum())

# Step 4
inc_reset = inc_idx.reset_index()

# Step 5
print("Index after reset:", inc_reset.index)
```

</details>
