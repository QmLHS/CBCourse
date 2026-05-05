# Good practices for loading a CSV file with Pandas

Loading a file correctly requires answering several questions **before** writing a
single line of Python. The procedure below works for any structured text file.

---

## Step 1 — Inspect the raw file

Before opening Python, open the file with a **text editor** (VS Code, TextEdit)
or from the **shell**:

```bash
# First 10 lines
head data/myfile.csv

# First 10 lines with non-printable characters visible (finds \r, \t, BOM)
cat -v -t -e data/myfile.csv | head

# If available, use the more informative bat
bat -A data/myfile.csv
```

What to look for:

- What is the **separator** between fields? (`,` `;` `\t` space)
- Does the **first row** contain column names?
- Are there **comment or description rows** at the top?
- Do numbers use a **comma or period** as the decimal separator?
- Are there **sentinel values** representing missing data (e.g. `9999-12-31`,
  `-99`, `N/D`, `n.a.`)?
- Are there **date columns**? In what format? (e.g. `DD/MM/YYYY`, `YYYY-MM-DD`)
- Is the file **compressed**? (`.csv.gz`, `.csv.bz2`)
  — Pandas handles these transparently, no extra step needed.

---

## Step 2 — Verify the encoding

From the shell:

```bash
file -I data/myfile.csv       # macOS / Linux
```

If the output shows `charset=iso-8859-1` or `charset=unknown-8bit`, the file is
not UTF-8 and you will need `encoding='iso-8859-1'`. If it shows `charset=utf-8`,
no encoding parameter is needed.

Without a shell, load the file without `encoding=` and immediately check whether
accented characters are readable. A `UnicodeDecodeError` confirms the file is
not UTF-8.

---

## Step 3 — Load a sample

Do not load the full file yet. Use `nrows=5` to read only a few rows and verify
your parameter choices:

```python
import pandas as pd

sample = pd.read_csv(
    "RawData/myfile.csv",
    delimiter = ";",
    decimal   = ",",
    encoding  = "iso-8859-1",
    nrows     = 5
)
```

---

## Step 4 — Inspect the sample

```python
print(sample.head())            # Do the values make sense?
sample.info()                   # shape, column names, dtypes, and non-null counts in one call
print(sample.dtypes)            # float64, int64, or object (= string)?
print(sample.columns.tolist())  # Column names read correctly?
print(sample.shape)             # Expected number of columns?
```

`.info()` is the single most informative call at this stage: it reports the number of rows, all column names, their dtype, and how many non-null values each has — letting you spot type problems and unexpected missing values at a glance.

**Diagnosing problems:**

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Wrong number of columns | Wrong separator | Change `delimiter=` |
| Numeric column has dtype `object` | Wrong decimal separator | Add `decimal=','` |
| Column names contain garbled characters | Wrong encoding | Add `encoding='iso-8859-1'` |
| Date column has dtype `object` | Dates not parsed | Add `parse_dates=['col']` |
| First row is data, not a header | No header in file | Add `names=['c1','c2',...]` |
| Extra unexpected rows at the top | Comment/description header | Add `skiprows=N` |

---

## Step 5 — Load the complete file

Once the sample looks correct, remove `nrows` and add all remaining parameters:

```python
dati = pd.read_csv(
    "RawData/myfile.csv",
    delimiter   = ";",
    decimal     = ",",
    encoding    = "iso-8859-1",
    na_values   = ["N/D", "-99", "9999-12-31"],
    parse_dates = ["data_inizio", "data_fine"],
    dayfirst    = True,          # DD/MM/YYYY date format
    index_col   = "id"           # optional: set a column as row index
)
```

---

## Step 6 — Verify dates

> **Golden rule:** always convert date columns **at load time** with `parse_dates=`
> inside `read_csv()`. Never leave them as strings and convert later.
> `pd.to_datetime()` is a fallback for cases `parse_dates` cannot handle.

`parse_dates=` handles most cases, but may fail silently, leaving the column as
`object`. Even when it succeeds, dates deserve a **visual inspection**: day and
month can be silently swapped, 2-digit years can land in the wrong century, and
sentinel values not in `na_values=` become `NaT` without any warning.

### 6a — Confirm the dtype

```python
dati.info()                         # date columns must show datetime64[ns], not object
print(dati["data_inizio"].dtype)    # double-check a specific column
```

### 6b — Inspect the values visually

Always compare a few parsed values against the raw file side by side:

```python
# Read the same rows as raw strings (no parsing) and compare
raw = pd.read_csv("RawData/myfile.csv", delimiter=";", nrows=5)
print(raw["data_inizio"])           # raw string, e.g. "25/03/2023"
print(dati["data_inizio"].head())   # parsed result, should be 2023-03-25
```

Things that look correct but are wrong:
- `01/03/2023` parsed as 3 January instead of 1 March (missing `dayfirst=True`)
- `23` parsed as 1923 instead of 2023 (2-digit year with `%y`)
- Values that were sentinel strings (e.g. `9999-12-31`) now showing as
  `NaT` — correct only if you listed them in `na_values=`

### 6c — Check the range

```python
print(dati["data_inizio"].min(), dati["data_inizio"].max())
```

The min and max should fall within the expected time span of your dataset.
`NaT` for either value means parsing produced all missing — the format string
does not match the file.

### 6d — Fallback: `pd.to_datetime()` after loading

Only if `parse_dates=` cannot handle the format, convert the column explicitly
as a second step:

```python
# European format: DD/MM/YYYY  (e.g. "25/03/2023")
dati["data_inizio"] = pd.to_datetime(dati["data_inizio"],
                                     format="%d/%m/%Y")

# ISO 8601: YYYY-MM-DD  (e.g. "2023-03-25") — inferred automatically in most cases
dati["data_fine"] = pd.to_datetime(dati["data_fine"])
```

Common format codes:

| Code | Meaning          | Example |
|:----:|:-----------------|:-------:|
| `%d` | Day (01–31)      | `25`    |
| `%m` | Month (01–12)    | `03`    |
| `%Y` | 4-digit year     | `2023`  |
| `%y` | 2-digit year     | `23`    |
| `%H` | Hour (00–23)     | `14`    |
| `%M` | Minute (00–59)   | `30`    |
| `%S` | Second (00–59)   | `00`    |

> **2-digit year warning:** `%y` maps 00–68 → 2000–2068 and 69–99 → 1969–1999.
> If your dataset spans a different range, correct the dates after conversion.

After any fix, repeat steps 6a–6c before moving on.

---

## Step 7 — Verify the final result

```python
print(dati.shape)            # expected (rows, columns)?
print(dati.dtypes)           # all types correct? dates show datetime64[ns]?
print(dati.describe())       # outliers, unexpected NaN?
print(dati.isnull().sum())   # missing count per column
```

If `describe()` shows a minimum or maximum clearly out of range (e.g. `-99` in an
age column, `9999` in a year), a sentinel value was not caught by `na_values=`.
Go back to Step 5 and add it.

---

## Summary

```
1. Inspect the raw file      →  text editor or shell (head, cat -A, bat)
2. Verify encoding           →  shell (file -I) or load attempt in Python
3. Load a sample             →  nrows=5
4. Inspect the sample        →  .info(), .head(), .dtypes, .columns.tolist(), .shape
5. Load the complete file    →  remove nrows, add all parameters
6. Check dates and types     →  .dtype, pd.to_datetime() if needed
7. Verify the final result   →  .shape, .dtypes, .describe(), .isnull().sum()
```

> **Practical rule:** if `.dtypes` shows `object` where you expected `float64`,
> the separator or decimal is wrong. If a date column remains `object` after
> loading, `parse_dates=` did not match — go back to Step 1 and re-read how the
> date is written in the raw file. If `.isnull().sum()` shows unexpected NaNs in
> a column that should be complete, a missing-value sentinel was not listed in
> `na_values=`.
