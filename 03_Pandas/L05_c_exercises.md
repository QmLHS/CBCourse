# Exercises — Pandas: Transforming a DataFrame

**Covered lecture:** L05_c

**Dataset:** `RawData/incidenti.csv` — Milan traffic incidents 2001--2016 (1920 rows, 6 columns:
`Zona`, `Incidenti`, `Anno`, `Morti`, `Mese`, `Feriti`).

---

## Exercise 1 — Descriptive statistics (difficulty: ★)

### Tasks

1. Load `RawData/incidenti.csv` and run `.describe()`.
2. From the output, report:
   - mean number of accidents per record
   - maximum deaths in a single record
   - 75th percentile of injuries (`Feriti`)
3. Using `groupby`, compute the **total** number of incidents per year.
4. Which year had the most incidents?  Which had the fewest?
5. Compute the **mean** monthly deaths (`Morti`) across all zones, per year.
   In which year was this mean the highest?

> **Hint:** Chain `.groupby(...)[...].mean()` for step 5.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

inc = pd.read_csv("RawData/incidenti.csv")
print(inc.describe())

by_year = inc.groupby('Anno')['Incidenti'].sum()
print("Worst year:", by_year.idxmax(), by_year.max())
print("Best year:", by_year.idxmin(), by_year.min())

mean_morti = inc.groupby('Anno')['Morti'].mean()
print("Highest mean deaths/month, year:", mean_morti.idxmax(),
      f"({mean_morti.max():.2f})")
```

</details>

---

## Exercise 2 — Missing values and type conversion (difficulty: ★★)

### Scenario

The `Zona` column is stored as `float64` because it contains missing values.
You need to create a clean integer version without losing rows.

### Tasks

1. Count the number of missing values in each column.
2. Create a copy of the DataFrame with all `NaN` rows dropped (`dropna()`).
   How many rows remain?
3. On the cleaned copy, convert `Zona` from `float64` to `int64`.
   Verify the new dtype.
4. On the **original** DataFrame (with missing values), create a new column
   `Zona_int` that holds the integer zone where known and `0` where `Zona` is missing.
5. Verify that `Zona_int` has no missing values.

> **Hint:** For step 4, initialise `inc['Zona_int'] = 0`, then use
> `.loc[inc['Zona'].notnull(), 'Zona_int'] = ...`.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

inc = pd.read_csv("RawData/incidenti.csv")

# Step 1
print(inc.isnull().sum())

# Step 2
inc_clean = inc.dropna()
print("Rows after dropna:", len(inc_clean))

# Step 3
inc_clean = inc_clean.copy()
inc_clean['Zona'] = inc_clean['Zona'].astype(int)
print("Zona dtype:", inc_clean['Zona'].dtype)

# Step 4
inc['Zona_int'] = 0
not_null = inc['Zona'].notnull()
inc.loc[not_null, 'Zona_int'] = inc.loc[not_null, 'Zona'].astype(int)

# Step 5
print("Missing in Zona_int:", inc['Zona_int'].isnull().sum())
```

</details>

---

## Exercise 3 — GroupBy analysis (difficulty: ★★)

### Scenario

A road safety officer wants to understand which city zone and which month of the year
are most dangerous.

### Tasks

1. Create `Zona_int` as in Exercise 2 (or reload the file and recreate it).
2. For each zone (excluding zone 0 = missing), compute the total number of
   incidents, deaths, and injuries across all years.
3. Rank zones by total incidents (highest first) and print the ranking.
4. Compute the total incidents per month across all zones and years.
   Which month is most dangerous?
5. For each zone, find the month with the highest total incidents.
   Print a table with columns `Zona_int`, `Mese`, `Incidenti`.

> **Hint:** For step 5, use `groupby(['Zona_int', 'Mese']).sum()` then
> group again by zone and use `.idxmax()`.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

inc = pd.read_csv("RawData/incidenti.csv")
inc['Zona_int'] = 0
not_null = inc['Zona'].notnull()
inc.loc[not_null, 'Zona_int'] = inc.loc[not_null, 'Zona'].astype(int)

# Step 2
by_zone = (inc[inc['Zona_int'] != 0]
           .groupby('Zona_int')[['Incidenti','Morti','Feriti']]
           .sum())

# Step 3
print(by_zone.sort_values('Incidenti', ascending=False))

# Step 4
by_month = inc.groupby('Mese')['Incidenti'].sum()
print("Most dangerous month:", by_month.idxmax())

# Step 5
by_zone_month = (inc[inc['Zona_int'] != 0]
                 .groupby(['Zona_int','Mese'])['Incidenti']
                 .sum()
                 .reset_index())
worst_idx = by_zone_month.groupby('Zona_int')['Incidenti'].idxmax()
print(by_zone_month.loc[worst_idx, ['Zona_int','Mese','Incidenti']].reset_index(drop=True))
```

</details>

---

## Exercise 4 — Binning and apply (difficulty: ★★★)

### Scenario

You want to classify each record by the season it belongs to
and study whether accident severity varies across seasons.

### Tasks

1. Create a column `ratio = Feriti / Incidenti` (injury rate per accident).
   Handle any records where `Incidenti == 0` by assigning `NaN`.
2. Use `pd.cut` to classify `Mese` into seasons:
   - months 1--3 → `'winter'`
   - months 4--6 → `'spring'`
   - months 7--9 → `'summer'`
   - months 10--12 → `'autumn'`
3. For each season, compute the mean `ratio`.
   Which season has the highest injury rate?
4. Use `.apply()` on the `ratio` column to create a `severity` column:
   - `'low'` if `ratio < 1.3`
   - `'medium'` if `1.3 <= ratio < 1.5`
   - `'high'` if `ratio >= 1.5`
5. Count the number of records per `(severity, season)` combination.

> **Hint:** For step 2, use `bins=[0, 3, 6, 9, 12]` and `right=True`.
> For step 1, use `inc['Incidenti'].replace(0, float('nan'))` as the denominator.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd
import numpy as np

inc = pd.read_csv("RawData/incidenti.csv")

# Step 1
denom = inc['Incidenti'].replace(0, np.nan)
inc['ratio'] = inc['Feriti'] / denom

# Step 2
inc['season'] = pd.cut(inc['Mese'],
                       bins=[0, 3, 6, 9, 12],
                       labels=['winter', 'spring', 'summer', 'autumn'],
                       right=True)

# Step 3
seasonal = inc.groupby('season')['ratio'].mean()
print(seasonal)
print("Highest injury rate:", seasonal.idxmax())

# Step 4
def classify(r):
    if r < 1.3:
        return 'low'
    if r < 1.5:
        return 'medium'
    return 'high'

inc['severity'] = inc['ratio'].apply(classify)

# Step 5
counts = inc.groupby(['severity', 'season']).size().unstack(fill_value=0)
print(counts)
```

</details>

---

## Exercise 5 — Pivot tables and extremes (difficulty: ★★★★)

### Scenario

You want to build a year × month summary and identify the single worst month in each year.

### Tasks

1. Build a pivot table with:
   - rows = `Anno`
   - columns = `Mese`
   - values = total `Incidenti` (use `aggfunc='sum'`)
2. Print the pivot table.  Which cell has the absolute maximum?
3. For each year, find the month with the highest total incidents.
   Build a DataFrame with columns `Anno`, `worst_month`, `incidents`.
4. Add a column `share` = worst-month incidents / that year's total incidents × 100.
   This tells you how concentrated the accidents are in the peak month.
5. Which year has the most "concentrated" peak month (highest `share`)?

> **Hint:** For step 3, use `pivot.idxmax(axis=1)` to get the worst month per row.

### Solution

<details>
<summary>Show solution</summary>

```python
import pandas as pd

inc = pd.read_csv("RawData/incidenti.csv")

# Step 1 and 2
pivot = pd.pivot_table(inc, index='Anno', columns='Mese',
                       values='Incidenti', aggfunc='sum')
print(pivot)
total_max = pivot.max().max()
year_max  = pivot.stack().idxmax()
print(f"Global maximum: {total_max} in year {year_max[0]}, month {year_max[1]}")

# Step 3
worst_month  = pivot.idxmax(axis=1)
worst_value  = pivot.max(axis=1)
yearly_total = pivot.sum(axis=1)

summary = pd.DataFrame({
    'worst_month': worst_month,
    'incidents':   worst_value,
})

# Step 4
summary['share'] = summary['incidents'] / yearly_total * 100

# Step 5
print(summary.sort_values('share', ascending=False))
print("Most concentrated year:", summary['share'].idxmax())
```

</details>
