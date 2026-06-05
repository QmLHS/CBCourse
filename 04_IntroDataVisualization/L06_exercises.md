# Exercises — Introduction to Data Visualization

**Covered lectures:** L06_a, L06_b

**Datasets** (inside `04_IntroDataVisualization/data/`):

| File | Notes |
|------|-------|
| `data/Grezzi.xls` | Multi-experiment growth curve dataset (see below) |

---

### About `Grezzi.xls`

This file collects batch-culture microbial growth experiments carried out over several years by different researchers in the same laboratory. Because the data were recorded independently, there is no single agreed format: sheet structure, time range, and sampling frequency all vary between experimenters.

The file contains **27 sheets**, one per experiment. Each sheet holds a time series with the following columns:

| Column | Meaning |
|--------|---------|
| `time` | Elapsed time since inoculation (hours) |
| `OD` | Optical density — a proxy for cell concentration |
| `Glc` | Glucose concentration (mM) |
| `etoh` | Ethanol concentration (mM) |
| `Glu` | Glutamate concentration (mM) |
| `AKG` | Alpha-ketoglutarate concentration (mM) |
| `Gly` | Glycine concentration (mM) |
| `Fum` | Fumarate concentration (mM) |

Sheet names encode the experiment metadata: a single uppercase letter identifies the research group or experimental batch (A–J, spanning multiple years), followed by the nitrogen source used (`Glut` for glutamate, `Amm` for ammonium sulphate), and an optional replicate index (e.g. `HAmm1`, `HAmm2`). This naming convention is the **only** place where this information is recorded — it is not stored as a column in the sheets themselves.

Not all measurements were taken at the same absolute times: some experimenters started recording from inoculation (t = 0 h), while others began mid-experiment. A handful of sheets also contain missing OD values at t = 0, where the spectrophotometer blank was read before cells were added to the cuvette.

The OD column deserves special attention. Optical density at 600 nm is a standard proxy for cell concentration: as cells multiply, the culture becomes more turbid and OD rises. In a batch culture with a fixed nutrient supply, growth does not continue indefinitely — it accelerates during the exponential phase, then slows as nutrients are exhausted and the population approaches its carrying capacity. The resulting OD vs time curve is characteristic: it follows a sigmoid (S-shaped) trajectory, rising steeply in the middle and levelling off at both ends.

---

## Exercise 1 — From raw spreadsheet to aligned growth curves (difficulty: ★★★★)

### Scenario

You have inherited the `Grezzi.xls` file from the lab archive. The long-term goal is to pool the metabolite concentration time series from all ammonium experiments into a single, coherent dataset — but because different groups started measuring at different points in the growth cycle, the time axes are not aligned and the series cannot be directly compared or merged. Before any pooling is possible, the time axes must be brought onto a shared reference. Your first task is therefore to consolidate the raw spreadsheet into a tidy dataframe, recover the experimental metadata hidden in the sheet names, and produce a time-aligned view of the ammonium OD curves.

<details>
<summary>Tasks</summary>

1. Load all 27 sheets into a single dataframe, preserving each sheet's name as an `exp` column. Restrict the data to the columns `exp`, `time`, and `OD`. Clean any missing values.

2. Recover the nitrogen source (`Glut` or `Amm`) from the experiment name and store it as a new column. Split the data by nitrogen source and verify that no observations were lost.

3. Align the ammonium OD time series onto a shared time axis and plot the result.

</details>

<details>
<summary>Step-by-step guidance</summary>

1. Use `pd.read_excel` with `sheet_name=None` and `header=1` to load the entire workbook as a dictionary of dataframes. Iterate over it, add a column `exp` to each sub-dataframe with the sheet name as its value, then concatenate everything into a single dataframe `dfDati`.

2. Keep only the columns `exp`, `time`, and `OD` in a new dataframe `dfOD`. Use `.info()` to identify columns with missing entries, then drop all rows where `OD` is `NaN` (in-place).

3. The experiment name follows the pattern `[LetterA-J][NutrientName][OptionalReplicate]`, where `NutrientName` is either `Glut` or `Amm`. Use a regular expression with `pandas.Series.str.extract` to extract `NutrientName` into a new column `fonte`. The tool [regex101.com](https://regex101.com) is useful for building and testing patterns interactively.

4. Create two dataframes — `dfODAmm` and `dfODGlut` — by filtering on `fonte`. Verify that the sum of their row counts equals the row count of `dfOD`.

5. Plot OD vs time for the ammonium experiments using a scatter plot. Are the curves aligned along the time axis?

6. Implement the logistic (sigmoid) function as `sigmoid(xIn, yMax, xMidpoint, kSteep)`:

    $$y(x) = \frac{y_{\max}}{1 + e^{-k_{\text{steep}} \cdot (x - x_{\text{mid}})}}$$

    where $y_{\max}$ is the carrying capacity, $x_{\text{mid}}$ is the inflection point (time at half-maximum growth), and $k_{\text{steep}}$ controls the steepness of the transition. Use [`scipy.optimize.curve_fit`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html) to fit it to the `HAmm1` experiment. Print the fitted parameters and the covariance matrix.

7. Loop over every unique experiment in `dfODAmm`. For each one, fit the sigmoid (use `p0=[25.0, 24.0, 0.25]` as initial guess) and store the three fitted parameters as new columns `yMax`, `xMid`, and `kStp` in `dfODAmm`.

    > You can assign a scalar value to a subset of rows using boolean indexing: `dfODAmm.loc[dfODAmm.exp == exp, "yMax"] = value`.

8. Compute a new column `timeShifted` by subtracting from each observation's `time` the difference between its experiment's `xMid` and the minimum `xMid` across all experiments, then adding back the maximum `xMid`. Plot OD vs `timeShifted` for all ammonium experiments and compare with the unaligned plot from step 5.

</details>
