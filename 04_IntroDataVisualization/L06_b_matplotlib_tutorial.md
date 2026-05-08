# Visualizzare i dati con Matplotlib

In questa lezione impariamo a produrre grafici in Python usando la libreria
`matplotlib`. Per gli esempi utilizziamo il dataset `MeteoMilano.csv`, che contiene
osservazioni meteorologiche giornaliere per la città di Milano.

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
```

---

## Caricare e preparare i dati

```python
df = pd.read_csv("MeteoMilano.csv",
                 parse_dates=["CET"])       # parse date column at load time
df.columns = df.columns.str.strip()        # remove leading/trailing spaces

df = df.rename(columns={
    "CET":               "date",
    "Temperatura maxC":  "tmax",
    "Temperatura mediaC":"tmean",
    "Temperatura minC":  "tmin",
    "Precipitazionimm":  "precip",
    "Mean Umidità":      "humidity",
})

df["month"]  = df["date"].dt.month
df["year"]   = df["date"].dt.year
df["precip"] = pd.to_numeric(df["precip"], errors="coerce")

df = df.dropna(subset=["tmax", "tmean", "tmin"])
print(df.shape)        # (1811, ...)
print(df.head())
# The dataset covers 2011–2015.
```

Il dataset contiene una riga per ogni giorno. Le colonne principali che useremo:

| Colonna    | Descrizione                        |
| :--------- | :--------------------------------- |
| `date`     | Data (tipo `datetime`)             |
| `tmax`     | Temperatura massima giornaliera °C |
| `tmean`    | Temperatura media giornaliera °C   |
| `tmin`     | Temperatura minima giornaliera °C  |
| `precip`   | Precipitazioni mm                  |
| `humidity` | Umidità relativa media %           |
| `month`    | Mese (1–12)                        |
| `year`     | Anno                               |

---

## Anatomia di una figura matplotlib

Matplotlib organizza ogni grafico in tre livelli gerarchici:

- **`Figure`** — il foglio. Contiene uno o più pannelli.
- **`Axes`** — un singolo pannello con il suo sistema di coordinate. È qui che
  vengono disegnati i dati. Non va confuso con `Axis` (i singoli righelli x/y).
- **`Artists`** — ogni elemento visibile: linee, barre, testo, tick, bordi…

### L'API orientata agli oggetti

Usiamo sempre la cosiddetta **OO API**: creiamo `fig` e `ax` come oggetti espliciti
e chiamiamo i metodi direttamente su di essi.

```python
fig, ax = plt.subplots()          # crea Figure e Axes
ax.plot([1, 2, 3], [4, 2, 5])    # disegna sui dati
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Primo grafico")
fig.savefig("primo.pdf", bbox_inches="tight")
plt.show()
```

`plt.subplots()` restituisce sempre una coppia `(fig, ax)`. Ogni modifica
al grafico avviene tramite metodi di `ax`; ogni operazione sulla figura
(dimensioni, salvataggio) tramite metodi di `fig`.

---

## Grafico a linee — `ax.plot()`

Connette i punti in ordine crescente di `x`. Adatto a **serie temporali** e
funzioni continue.

```python
# Selezioniamo un anno per chiarezza
df_2015 = df[df["year"] == 2015].copy()

fig, ax = plt.subplots(figsize=(10, 4))

ax.plot(df_2015["date"], df_2015["tmean"],
        color="steelblue", linewidth=1.2, label="Mean")
ax.plot(df_2015["date"], df_2015["tmax"],
        color="#E41A1C", linewidth=0.8,
        linestyle="--", label="Max")
ax.plot(df_2015["date"], df_2015["tmin"],
        color="#377EB8", linewidth=0.8,
        linestyle=":", label="Min")

ax.set_xlabel("Date")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Milan — daily temperature 2015")
ax.legend()
fig.savefig("line_temperature.pdf", bbox_inches="tight")
plt.show()
```

### Parametri principali di `ax.plot()`

| Parametro    | Descrizione                                  | Esempi                  |
| :----------- | :------------------------------------------- | :---------------------- |
| `color`      | Colore della linea (nome, hex, tupla RGB)    | `"steelblue"`, `"#E41A1C"` |
| `linewidth`  | Spessore in punti                            | `0.8`, `1.5`            |
| `linestyle`  | Tratteggio                                   | `"-"`, `"--"`, `":"`, `"-."` |
| `marker`     | Simbolo per ogni punto                       | `"o"`, `"s"`, `"^"`    |
| `markersize` | Dimensione del marker                        | `4`, `8`                |
| `alpha`      | Trasparenza (0 = invisibile, 1 = opaco)      | `0.6`                   |
| `label`      | Testo per la legenda                         | `"Mean temp."`          |

### Colore della linea

Il parametro `color` accetta nomi CSS (`"steelblue"`, `"tomato"`, `"black"`),
codici esadecimali (`"#E41A1C"`) o tuple RGB normalizzate (`(0.2, 0.6, 0.8)`).

```python
# Linea tratteggiata con colore esadecimale e spessore aumentato
ax.plot(df_2015["date"], df_2015["tmean"],
        color="#4DAF4A", linewidth=2.0, linestyle="--")
```

---

## Scatter plot — `ax.scatter()`

Rappresenta coppie di valori come punti. Adatto a esplorare **relazioni tra due
variabili continue**.

```python
fig, ax = plt.subplots(figsize=(6, 5))

sc = ax.scatter(df["tmin"], df["tmax"],
                c=df["month"],      # codifica il mese con il colore
                cmap="RdYlBu_r",   # colormap divergente
                alpha=0.4,
                s=12)              # dimensione in pt^2

fig.colorbar(sc, ax=ax, label="Month")
ax.set_xlabel("Min temperature (°C)")
ax.set_ylabel("Max temperature (°C)")
ax.set_title("Daily Tmin vs Tmax — Milan")
fig.savefig("scatter_tminmax.pdf", bbox_inches="tight")
plt.show()
```

### Mappare una terza variabile

`ax.scatter()` permette di mappare una variabile aggiuntiva sul **colore** (`c`)
e sulla **dimensione** (`s`) di ogni punto:

```python
ax.scatter(df["tmin"], df["tmax"],
           c=df["humidity"],    # terza variabile sul colore
           cmap="viridis",
           s=df["precip"] + 5, # quarta variabile sulla dimensione
           alpha=0.5)
```

### Parametri principali di `ax.scatter()`

| Parametro | Descrizione                             |
| :-------- | :-------------------------------------- |
| `c`       | Valore di colore per ogni punto (array) |
| `cmap`    | Nome della colormap                     |
| `s`       | Dimensione per ogni punto (pt²)         |
| `alpha`   | Trasparenza                             |
| `marker`  | Simbolo del punto                       |

---

## Grafico a barre — `ax.bar()` / `ax.barh()`

Confronta valori tra **gruppi categoriali**.

### Barre verticali - `ax.bar()`

```python
# Temperatura media mensile
monthly_mean = df.groupby("month")["tmean"].mean()
month_names  = ["Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"]

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(month_names, monthly_mean,
       color="steelblue", edgecolor="white", width=0.7)
ax.set_xlabel("Month")
ax.set_ylabel("Mean temperature (°C)")
ax.set_title("Milan — monthly mean temperature")
fig.savefig("bar_monthly.pdf", bbox_inches="tight")
plt.show()
```

### Barre orizzontali — `ax.barh()`

```python
fig, ax = plt.subplots(figsize=(5, 6))
ax.barh(month_names, monthly_mean, color="steelblue")
ax.set_xlabel("Mean temperature (°C)")
ax.set_title("Milan — monthly mean temperature")
fig.savefig("barh_monthly.pdf", bbox_inches="tight")
plt.show()
```

### Barre affiancate (più serie)

```python
monthly_2014 = df[df["year"]==2014].groupby("month")["tmean"].mean()
monthly_2015 = df[df["year"]==2015].groupby("month")["tmean"].mean()

x      = np.arange(12)
width  = 0.35

fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(x - width/2, monthly_2014, width, label="2014",
       color="#377EB8", edgecolor="white")
ax.bar(x + width/2, monthly_2015, width, label="2015",
       color="#E41A1C", edgecolor="white")

ax.set_xticks(x)
ax.set_xticklabels(month_names)
ax.set_ylabel("Mean temperature (°C)")
ax.set_title("Monthly mean temperature: 2014 vs 2015")
ax.legend()
fig.savefig("bar_grouped.pdf", bbox_inches="tight")
plt.show()
```

---

## Istogramma — `ax.hist()`

Mostra la **distribuzione** di una variabile continua suddividendola in intervalli.

```python
fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(df["tmax"], bins=30,
        color="steelblue", edgecolor="white")
ax.set_xlabel("Max temperature (°C)")
ax.set_ylabel("Count")
ax.set_title("Distribution of daily Tmax — Milan")
fig.savefig("hist_tmax.pdf", bbox_inches="tight")
plt.show()
```

### Confrontare due distribuzioni

```python
tmax_2014 = df[df["year"] == 2014]["tmax"]
tmax_2015 = df[df["year"] == 2015]["tmax"]

fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(tmax_2014, bins=25, alpha=0.6,
        color="#377EB8", edgecolor="white", label="2014")
ax.hist(tmax_2015, bins=25, alpha=0.6,
        color="#E41A1C", edgecolor="white", label="2015")
ax.set_xlabel("Max temperature (°C)")
ax.set_ylabel("Count")
ax.set_title("Tmax distribution: 2014 vs 2015")
ax.legend()
fig.savefig("hist_compare.pdf", bbox_inches="tight")
plt.show()
```

### Parametri principali di `ax.hist()`

| Parametro  | Descrizione                                   | Default |
| :--------- | :-------------------------------------------- | :------ |
| `bins`     | Numero di barre (intero) o bordi espliciti    | 10      |
| `density`  | Se `True`, l'area totale è normalizzata a 1   | `False` |
| `alpha`    | Trasparenza (utile per sovrapporre distribuzioni) | 1.0 |
| `edgecolor`| Colore del bordo di ogni barra               | `None`  |

---

## Box plot — `ax.boxplot()`

Rappresenta la distribuzione con mediana, quartili e outlier. Utile per
**confrontare distribuzioni** tra più gruppi.

```python
# Raggruppiamo tmax per mese
data_by_month = [df[df["month"] == m]["tmax"].dropna().values
                 for m in range(1, 13)]

fig, ax = plt.subplots(figsize=(10, 5))
bp = ax.boxplot(data_by_month,
                labels=month_names,
                patch_artist=True,       # fill boxes with color
                medianprops=dict(color="white", linewidth=2))

# Color each box
colors = plt.cm.RdYlBu_r(np.linspace(0.1, 0.9, 12))
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)

ax.set_xlabel("Month")
ax.set_ylabel("Max temperature (°C)")
ax.set_title("Distribution of daily Tmax by month — Milan")
fig.savefig("boxplot_monthly.pdf", bbox_inches="tight")
plt.show()
```

### Violin plot — `ax.violinplot()`

Aggiunge una stima della densità (kernel density estimate) attorno al box.
Rivela la forma della distribuzione in modo più ricco.

```python
fig, ax = plt.subplots(figsize=(10, 5))
vp = ax.violinplot(data_by_month,
                   positions=range(1, 13),
                   showmedians=True,
                   showextrema=True)

for body in vp["bodies"]:
    body.set_facecolor("steelblue")
    body.set_alpha(0.7)

ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names)
ax.set_xlabel("Month")
ax.set_ylabel("Max temperature (°C)")
ax.set_title("Violin plot of daily Tmax by month — Milan")
fig.savefig("violin_monthly.pdf", bbox_inches="tight")
plt.show()
```

---

## Bande di incertezza — `ax.fill_between()`

Disegna una **banda continua** attorno a una curva. Ideale per visualizzare
intervalli di confidenza o variabilità.

```python
# Media e deviazione standard mensile
monthly_stats = df.groupby(df["date"].dt.to_period("M"))["tmean"].agg(["mean", "std"])
monthly_stats.index = pd.PeriodIndex(monthly_stats.index).to_timestamp()

fig, ax = plt.subplots(figsize=(10, 4))

ax.fill_between(monthly_stats.index,
                monthly_stats["mean"] - monthly_stats["std"],
                monthly_stats["mean"] + monthly_stats["std"],
                alpha=0.25, color="steelblue", label="±1 SD")
ax.plot(monthly_stats.index, monthly_stats["mean"],
        color="steelblue", linewidth=1.5, label="Monthly mean")

ax.set_xlabel("Date")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Monthly mean temperature ± 1 SD — Milan")
ax.legend()
fig.savefig("ribbon.pdf", bbox_inches="tight")
plt.show()
```

Per barre di errore su punti discreti si usa `ax.errorbar()`:

```python
monthly_m = df.groupby("month")["tmean"].mean()
monthly_s = df.groupby("month")["tmean"].std()

fig, ax = plt.subplots(figsize=(8, 4))
ax.errorbar(range(1, 13), monthly_m, yerr=monthly_s,
            fmt="o", capsize=4, color="steelblue",
            markersize=6, linewidth=1.2)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names)
ax.set_xlabel("Month")
ax.set_ylabel("Mean temperature (°C)")
ax.set_title("Monthly mean ± 1 SD — Milan")
fig.savefig("errorbar.pdf", bbox_inches="tight")
plt.show()
```

---

## Pannelli multipli — `plt.subplots()`

`plt.subplots(nrows, ncols)` crea una griglia di `Axes` organizzati in righe e
colonne. Restituisce `(fig, axes)` dove `axes` è un array NumPy 2D indicizzato
con `[riga, colonna]`.

```python
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(11, 7))

# Pannello [0,0] — line plot
df_2015 = df[df["year"] == 2015]
axes[0, 0].plot(df_2015["date"], df_2015["tmean"],
                color="steelblue", linewidth=1.0)
axes[0, 0].set_title("Daily mean temperature 2015")
axes[0, 0].set_ylabel("°C")

# Pannello [0,1] — scatter
axes[0, 1].scatter(df["tmin"], df["tmax"],
                   c=df["month"], cmap="RdYlBu_r",
                   alpha=0.3, s=8)
axes[0, 1].set_title("Tmin vs Tmax")
axes[0, 1].set_xlabel("Tmin (°C)")
axes[0, 1].set_ylabel("Tmax (°C)")

# Pannello [1,0] — bar chart
axes[1, 0].bar(month_names, monthly_mean,
               color="steelblue", edgecolor="white")
axes[1, 0].set_title("Monthly mean temperature")
axes[1, 0].set_ylabel("°C")
axes[1, 0].tick_params(axis="x", rotation=45)

# Pannello [1,1] — histogram
axes[1, 1].hist(df["tmax"], bins=30,
                color="steelblue", edgecolor="white")
axes[1, 1].set_title("Distribution of Tmax")
axes[1, 1].set_xlabel("°C")
axes[1, 1].set_ylabel("Count")

fig.tight_layout()
fig.savefig("subplots.pdf", bbox_inches="tight")
plt.show()
```

`fig.tight_layout()` regola automaticamente lo spazio tra i pannelli per evitare
che le etichette si sovrappongano.

---

## Personalizzare il grafico

### Etichette — `set_xlabel()`, `set_ylabel()`, `set_title()`

```python
ax.set_xlabel("Date",            fontsize=12)
ax.set_ylabel("Temperature (°C)", fontsize=12)
ax.set_title("Milan daily temperatures",
             fontsize=14, fontweight="bold")
```

### Tick e tick labels

```python
import matplotlib.ticker as ticker

# Impostare le tacche manualmente
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names, rotation=45, ha="right")

# Formattare le etichette numeriche
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f °C"))

# Dimensione font dei tick
ax.tick_params(axis="both", labelsize=10)
```

### Spines — rimuovere i bordi superflui

```python
# Bordo superiore e destro sono visual noise nei grafici scientifici
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
```

### Legenda

```python
ax.plot(dates, tmean, label="Mean", color="steelblue")
ax.plot(dates, tmax,  label="Max",  color="#E41A1C")

ax.legend(loc="upper left",          # posizione
          frameon=False,             # rimuove il bordo
          fontsize=10)
```

Posizioni comuni: `"best"`, `"upper right"`, `"upper left"`, `"lower right"`,
`"lower left"`, `"center"`.

### Scale degli assi

```python
# Limiti
ax.set_xlim(0, 12)
ax.set_ylim(-10, 40)

# Scala logaritmica
ax.set_yscale("log")
```

### Colori

Matplotlib accetta colori in quattro formati:

| Formato          | Esempio                  |
| :--------------- | :----------------------- |
| Nome CSS         | `"steelblue"`, `"tomato"` |
| Codice hex       | `"#E41A1C"`, `"#377EB8"` |
| Tupla RGB [0,1]  | `(0.2, 0.6, 0.8)`        |
| Grayscale [0,1]  | `"0.5"` (stringa)        |

Per le colormap: `plt.cm.viridis`, `plt.cm.RdBu_r`, `plt.cm.Set1`, …

```python
# Estrarre un colore da una colormap
colors = plt.cm.Set1(np.linspace(0, 1, 5))   # 5 colori distinti

for i, year in enumerate(df["year"].unique()):
    subset = df[df["year"] == year]
    ax.plot(subset["month_num"], subset["tmean"],
            color=colors[i], label=str(year))
```

### Stile globale — `rcParams`

Per impostare uno stile coerente per tutti i grafici in uno script:

```python
plt.rcParams.update({
    "figure.dpi":       150,
    "font.size":        11,
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "axes.grid":        True,
    "grid.alpha":       0.3,
})
```

In alternativa si può usare un tema predefinito:

```python
plt.style.use("seaborn-v0_8-whitegrid")   # tema pulito con griglia
plt.style.use("ggplot")                    # palette simile a ggplot2
```

---

## Salvare il grafico

La funzione `fig.savefig()` salva la figura su file. Il formato viene dedotto
dall'estensione del nome.

```python
fig.savefig("output.pdf", bbox_inches="tight")
fig.savefig("output.svg", bbox_inches="tight")
fig.savefig("output.png", dpi=300, bbox_inches="tight")
```

| Parametro       | Descrizione                                      | Default  |
| :-------------- | :----------------------------------------------- | :------- |
| `bbox_inches`   | `"tight"` ritaglia i margini bianchi eccessivi   | `None`   |
| `dpi`           | Risoluzione per formati raster (PNG, JPEG)       | 100      |
| `transparent`   | Sfondo trasparente (utile per SVG/PNG)           | `False`  |
| `facecolor`     | Colore di sfondo della figura                    | `"white"`|

> **Regola pratica:** usare sempre `bbox_inches="tight"` per evitare che le
> etichette vengano tagliate. Usare PDF o SVG per grafici destinati a
> pubblicazione o presentazioni Beamer.

---

## Un esempio completo

Partiamo dai dati grezzi e produciamo una figura a due pannelli pronta per la
pubblicazione.

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# --- Caricamento e pulizia ---
df = pd.read_csv("MeteoMilano.csv",
                 parse_dates=["CET"])
df.columns = df.columns.str.strip()
df = df.rename(columns={
    "CET":               "date",
    "Temperatura maxC":  "tmax",
    "Temperatura mediaC":"tmean",
    "Temperatura minC":  "tmin",
    "Precipitazionimm":  "precip",
})
df["month"]  = df["date"].dt.month
df["year"]   = df["date"].dt.year
df["precip"] = pd.to_numeric(df["precip"], errors="coerce")
df = df.dropna(subset=["tmax", "tmean", "tmin"])

month_names = ["Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]

# --- Dati aggregati ---
monthly_mean = df.groupby("month")["tmean"].mean()
monthly_std  = df.groupby("month")["tmean"].std()

# --- Figura ---
plt.rcParams.update({"font.size": 11})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

# Pannello sinistro — serie temporale 2015 con banda ±1SD mensile
df_2015 = df[df["year"] == 2015].copy()

ax1.fill_between(range(1, 13),
                 monthly_mean - monthly_std,
                 monthly_mean + monthly_std,
                 alpha=0.2, color="steelblue", label="±1 SD (all years)")
ax1.plot(df_2015["month"], df_2015["tmean"],
         color="steelblue", linewidth=1.0, alpha=0.7, label="Daily 2015")
ax1.plot(range(1, 13), monthly_mean,
         color="#E41A1C", linewidth=2.0, label="Monthly mean")

ax1.set_xticks(range(1, 13))
ax1.set_xticklabels(month_names, rotation=45, ha="right")
ax1.set_ylabel("Temperature (°C)")
ax1.set_title("Daily temperature — 2015 vs long-term mean")
ax1.legend(fontsize=9, frameon=False)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# Pannello destro — box plot mensile
data_by_month = [df[df["month"] == m]["tmax"].dropna().values
                 for m in range(1, 13)]

bp = ax2.boxplot(data_by_month, labels=month_names,
                 patch_artist=True,
                 medianprops=dict(color="white", linewidth=1.8),
                 flierprops=dict(marker=".", markersize=3,
                                 markerfacecolor="gray", alpha=0.4))

cmap = plt.cm.RdYlBu_r
for patch, frac in zip(bp["boxes"], np.linspace(0.1, 0.9, 12)):
    patch.set_facecolor(cmap(frac))
    patch.set_alpha(0.85)

ax2.set_xlabel("Month")
ax2.set_ylabel("Max temperature (°C)")
ax2.set_title("Distribution of daily Tmax by month")
ax2.tick_params(axis="x", rotation=45)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

# --- Titolo e salvataggio ---
fig.suptitle("Milan weather — MeteoMilano dataset",
             fontsize=13, fontweight="bold", y=1.02)
fig.tight_layout()
fig.savefig("meteo_milan_publication.pdf", bbox_inches="tight")
fig.savefig("meteo_milan_publication.png", dpi=300, bbox_inches="tight")
plt.show()
```

---

## Riepilogo delle funzioni principali

### Creazione e struttura

| Funzione / metodo                                | Scopo                                              |
| :----------------------------------------------- | :------------------------------------------------- |
| `plt.subplots(nrows, ncols, figsize)`            | Crea Figure e griglia di Axes                      |
| `fig.tight_layout()`                             | Regola automaticamente lo spazio tra pannelli      |
| `fig.savefig(path, bbox_inches, dpi)`            | Salva la figura su file                            |
| `plt.style.use(name)`                            | Applica uno stile globale                          |
| `plt.rcParams.update({...})`                     | Modifica parametri globali                         |

### Tipi di grafico

| Metodo                                           | Scopo                        | Estetiche principali                        |
| :----------------------------------------------- | :--------------------------- | :------------------------------------------ |
| `ax.plot(x, y)`                                  | Grafico a linee              | `color`, `linewidth`, `linestyle`, `marker`, `label` |
| `ax.scatter(x, y)`                               | Scatter plot                 | `c`, `cmap`, `s`, `alpha`, `marker`         |
| `ax.bar(x, height)` / `ax.barh(y, width)`        | Barre verticali / orizzontali | `color`, `edgecolor`, `width`               |
| `ax.hist(x, bins)`                               | Istogramma                   | `bins`, `density`, `alpha`, `edgecolor`     |
| `ax.boxplot(data, labels)`                       | Box plot                     | `patch_artist`, `medianprops`, `flierprops` |
| `ax.violinplot(data, positions)`                 | Violin plot                  | `showmedians`, `showextrema`                |
| `ax.errorbar(x, y, yerr)`                        | Punti con barre di errore    | `fmt`, `capsize`, `color`                   |
| `ax.fill_between(x, y1, y2)`                     | Banda di incertezza          | `alpha`, `color`                            |
| `ax.imshow(matrix, cmap, vmin, vmax)`            | Heatmap                      | `aspect`, `cmap`, `vmin`, `vmax`            |

### Etichette e assi

| Metodo                                           | Scopo                                             |
| :----------------------------------------------- | :------------------------------------------------ |
| `ax.set_xlabel(label, fontsize)`                 | Etichetta asse x                                  |
| `ax.set_ylabel(label, fontsize)`                 | Etichetta asse y                                  |
| `ax.set_title(title, fontsize, fontweight)`      | Titolo del pannello                               |
| `fig.suptitle(title)`                            | Titolo della figura (sopra tutti i pannelli)      |
| `ax.set_xlim(min, max)` / `ax.set_ylim()`       | Limiti degli assi                                 |
| `ax.set_xticks(ticks)` / `ax.set_yticks()`      | Posizione delle tacche                            |
| `ax.set_xticklabels(labels, rotation)`          | Etichette delle tacche                            |
| `ax.tick_params(axis, labelsize, rotation)`      | Stile delle tacche                                |
| `ax.set_xscale("log")` / `ax.set_yscale("log")`| Scala logaritmica                                 |
| `ax.legend(loc, frameon, fontsize)`              | Legenda                                           |

### Colormap e colori

| Nome colormap    | Tipo        | Uso tipico                              |
| :--------------- | :---------- | :-------------------------------------- |
| `viridis`        | Sequenziale | Dati ordinati, accessibile              |
| `plasma`         | Sequenziale | Alternativa a viridis                   |
| `Blues`, `Reds`  | Sequenziale | Intensità di un singolo canale          |
| `RdBu_r`         | Divergente  | Valori attorno a zero (log2 FC, z-score)|
| `RdYlBu_r`       | Divergente  | Temperature, anomalie climatiche        |
| `Set1`, `Set2`   | Qualitativo | Categorie (≤ 8 gruppi)                 |
| `tab10`          | Qualitativo | Default matplotlib per categorie        |

### Personalizzazione

| Metodo                                           | Scopo                                             |
| :----------------------------------------------- | :------------------------------------------------ |
| `ax.spines["top"].set_visible(False)`            | Rimuove il bordo superiore                        |
| `ax.spines["right"].set_visible(False)`          | Rimuove il bordo destro                           |
| `ax.grid(True, alpha, linestyle)`                | Aggiunge la griglia                               |
| `fig.colorbar(mappable, ax, label)`              | Aggiunge la barra dei colori                      |
| `ax.annotate(text, xy, xytext, arrowprops)`      | Aggiunge un'annotazione con freccia               |
