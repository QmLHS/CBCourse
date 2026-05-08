import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("lecturesOliveFluo")

dCols = {
    "text":    "#CFD4C5",
    "bg":      "#3B3C36",
    "struct":  "#D0FF14",
    "alert":   "#7FFFD4",
    "example": "#FFD700",
    "red":     "#F88379",
    "orange":  "#FF7F00",
    "pink":    "#FFB7C5",
    "teal":    "#3AB09E",
}

# ---------- data ----------
df = pd.read_csv("MeteoMilano.csv", parse_dates=["CET"])
df.columns = df.columns.str.strip()
df = df.rename(columns={
    "CET":                "date",
    "Temperatura maxC":   "tmax",
    "Temperatura mediaC": "tmean",
    "Temperatura minC":   "tmin",
    "Precipitazionimm":   "precip",
    "Mean Umidità":       "humidity",
})
df["month"]  = df["date"].dt.month
df["year"]   = df["date"].dt.year
df["precip"] = pd.to_numeric(df["precip"], errors="coerce")
df = df.dropna(subset=["tmax", "tmean", "tmin"])

month_names   = ["Jan","Feb","Mar","Apr","May","Jun",
                 "Jul","Aug","Sep","Oct","Nov","Dec"]
monthly_mean  = df.groupby("month")["tmean"].mean()
monthly_std   = df.groupby("month")["tmean"].std()
data_by_month = [df[df["month"] == m]["tmax"].dropna().values
                 for m in range(1, 13)]

def tidy(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

FIG  = dict(figsize=(7, 4))
SAVE = dict(bbox_inches="tight")

# ================================================================
# 1 — Line plot  (single series)
# ================================================================
df_2015 = df[df["year"] == 2015]

fig, ax = plt.subplots(**FIG)
ax.plot(df_2015["date"], df_2015["tmean"],
        color=dCols["alert"], linewidth=1.2)
ax.set_xlabel("Date")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Line Plot")
tidy(ax)
fig.tight_layout()
fig.savefig("plot_line_minimal.pdf", **SAVE)
plt.close()

# ================================================================
# 2 — Scatter plot  (single color, no color aesthetic)
# ================================================================
fig, ax = plt.subplots(**FIG)
ax.scatter(df["tmin"], df["tmax"],
           color=dCols["alert"], alpha=0.35, s=8)
ax.set_xlabel("Min temperature (°C)")
ax.set_ylabel("Max temperature (°C)")
ax.set_title("Scatter Plot")
tidy(ax)
fig.tight_layout()
fig.savefig("plot_scatter_minimal.pdf", **SAVE)
plt.close()

# ================================================================
# 3 — Horizontal bar chart  (sorted decreasing top → bottom)
# ================================================================
# sort ascending: barh draws first entry at the bottom, last at the top
eventi_counts = df["Eventi"].value_counts().sort_values(ascending=True)

abbr = {"Nebbia": "Neb", "Pioggia": "Pio",
        "Temporale": "Tem", "Neve": "Nev", "Grandine": "Gra"}
labels = ["-".join(abbr.get(w, w) for w in e.split("-"))
          for e in eventi_counts.index]

fig, ax = plt.subplots(figsize=(7, 5))
ax.barh(labels, eventi_counts.values,
        color=dCols["alert"], edgecolor=dCols["bg"], height=0.7)
ax.set_xlabel("Days")
ax.set_title("Horizontal Bar Chart")
tidy(ax)
fig.tight_layout()
fig.savefig("plot_barh_minimal.pdf", **SAVE)
plt.close()

# ================================================================
# 4 — Histogram  (single distribution)
# ================================================================
fig, ax = plt.subplots(**FIG)
ax.hist(df["tmax"], bins=30,
        color=dCols["alert"], edgecolor=dCols["bg"])
ax.set_xlabel("Max temperature (°C)")
ax.set_ylabel("Count")
ax.set_title("Histogram")
tidy(ax)
fig.tight_layout()
fig.savefig("plot_histogram_minimal.pdf", **SAVE)
plt.close()

# ================================================================
# 5 — Box plot  (uniform color, no color encoding)
# ================================================================
fig, ax = plt.subplots(**FIG)
ax.boxplot(data_by_month,
           tick_labels=month_names,
           patch_artist=True,
           medianprops=dict(color=dCols["text"],  linewidth=2.0),
           whiskerprops=dict(color=dCols["text"]),
           capprops=dict(color=dCols["text"]),
           boxprops=dict(facecolor=dCols["alert"], edgecolor=dCols["text"]),
           flierprops=dict(marker=".", markersize=3,
                           markerfacecolor=dCols["text"], alpha=0.4))
ax.set_xlabel("Month")
ax.set_ylabel("Max temperature (°C)")
ax.set_title("Box Plot")
ax.tick_params(axis="x", rotation=45)
tidy(ax)
fig.tight_layout()
fig.savefig("plot_boxplot_minimal.pdf", **SAVE)
plt.close()

# ================================================================
# 6 — Violin plot
# ================================================================
fig, ax = plt.subplots(**FIG)
vp = ax.violinplot(data_by_month,
                   positions=range(1, 13),
                   showmedians=True,
                   showextrema=False)
for body in vp["bodies"]:
    body.set_facecolor(dCols["alert"])
    body.set_alpha(0.7)
vp["cmedians"].set_color(dCols["bg"])
vp["cmedians"].set_linewidth(2.0)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names, rotation=45, ha="right")
ax.set_xlabel("Month")
ax.set_ylabel("Max temperature (°C)")
ax.set_title("Violin Plot")
tidy(ax)
fig.tight_layout()
fig.savefig("plot_violin_minimal.pdf", **SAVE)
plt.close()

# ================================================================
# 7 — Error bars & ribbon
# ================================================================
x = np.arange(1, 13)

fig, ax = plt.subplots(**FIG)
ax.fill_between(x,
                monthly_mean - monthly_std,
                monthly_mean + monthly_std,
                alpha=0.25, color=dCols["alert"])
ax.plot(x, monthly_mean, color=dCols["alert"], linewidth=1.5)
ax.errorbar(x, monthly_mean, yerr=monthly_std,
            fmt="none", capsize=4,
            color=dCols["struct"], linewidth=1.0)
ax.set_xticks(x)
ax.set_xticklabels(month_names, rotation=45, ha="right")
ax.set_xlabel("Month")
ax.set_ylabel("Mean temperature (°C)")
ax.set_title("Error Bars & Ribbon")
tidy(ax)
fig.tight_layout()
fig.savefig("plot_errorbars_minimal.pdf", **SAVE)
plt.close()

# ================================================================
# 8 — Heatmap
# ================================================================
pivot = df.pivot_table(values="tmax", index="month",
                       columns="year", aggfunc="mean")

fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(pivot.values,
               aspect="auto",
               cmap="RdYlBu_r",
               vmin=df["tmax"].quantile(0.05),
               vmax=df["tmax"].quantile(0.95))
fig.colorbar(im, ax=ax, label="Mean Tmax (°C)")
ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(pivot.columns)
ax.set_yticks(range(12))
ax.set_yticklabels(month_names)
ax.set_xlabel("Year")
ax.set_ylabel("Month")
ax.set_title("Heatmap")
fig.tight_layout()
fig.savefig("plot_heatmap_minimal.pdf", **SAVE)
plt.close()
