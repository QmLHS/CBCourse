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
df = pd.read_csv("MeteoMilano.csv")
df.columns = df.columns.str.strip()
df = df.rename(columns={
    "CET":                "date",
    "Temperatura maxC":   "tmax",
    "Temperatura mediaC": "tmean",
    "Temperatura minC":   "tmin",
    "Precipitazionimm":   "precip",
    "Mean Umidità":       "humidity",
})
df["date"]   = pd.to_datetime(df["date"])
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

FIG = dict(figsize=(7, 4))
SAVE = dict(bbox_inches="tight")

# ================================================================
# 1 — Line plot
# ================================================================
df_2015 = df[df["year"] == 2015]

fig, ax = plt.subplots(**FIG)
ax.plot(df_2015["date"], df_2015["tmean"],
        color=dCols["alert"], linewidth=1.2, label="Mean")
ax.plot(df_2015["date"], df_2015["tmax"],
        color=dCols["red"], linewidth=0.8, linestyle="--", label="Max")
ax.plot(df_2015["date"], df_2015["tmin"],
        color=dCols["teal"], linewidth=0.8, linestyle=":", label="Min")
ax.set_xlabel("Date")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Line Plot — daily temperature 2015")
ax.legend(frameon=False)
tidy(ax)
fig.tight_layout()
fig.savefig("plot_line.pdf", **SAVE)
plt.close()

# ================================================================
# 2 — Scatter plot
# ================================================================
fig, ax = plt.subplots(**FIG)
sc = ax.scatter(df["tmin"], df["tmax"],
                c=df["month"], cmap="RdYlBu_r",
                alpha=0.45, s=12)
fig.colorbar(sc, ax=ax, label="Month")
ax.set_xlabel("Min temperature (°C)")
ax.set_ylabel("Max temperature (°C)")
ax.set_title("Scatter Plot — Tmin vs Tmax")
tidy(ax)
fig.tight_layout()
fig.savefig("plot_scatter.pdf", **SAVE)
plt.close()

# ================================================================
# 3 — Bar chart
# ================================================================
fig, ax = plt.subplots(**FIG)
ax.bar(month_names, monthly_mean,
       color=dCols["alert"], edgecolor=dCols["bg"], width=0.7)
ax.set_xlabel("Month")
ax.set_ylabel("Mean temperature (°C)")
ax.set_title("Bar Chart — monthly mean temperature")
ax.tick_params(axis="x", rotation=45)
tidy(ax)
fig.tight_layout()
fig.savefig("plot_bar.pdf", **SAVE)
plt.close()

# ================================================================
# 4 — Histogram
# ================================================================
fig, ax = plt.subplots(**FIG)
ax.hist(df[df["year"] == 2014]["tmax"], bins=25, alpha=0.7,
        color=dCols["alert"], edgecolor=dCols["bg"], label="2014")
ax.hist(df[df["year"] == 2015]["tmax"], bins=25, alpha=0.7,
        color=dCols["red"], edgecolor=dCols["bg"], label="2015")
ax.set_xlabel("Max temperature (°C)")
ax.set_ylabel("Count")
ax.set_title("Histogram — Tmax distribution")
ax.legend(frameon=False)
tidy(ax)
fig.tight_layout()
fig.savefig("plot_histogram.pdf", **SAVE)
plt.close()

# ================================================================
# 5 — Box plot
# ================================================================
monthly_tmax_mean = df.groupby("month")["tmax"].mean()
cmap = plt.cm.RdYlBu_r
norm = plt.Normalize(vmin=monthly_tmax_mean.min(), vmax=monthly_tmax_mean.max())

fig, ax = plt.subplots(**FIG)
bp = ax.boxplot(data_by_month,
                tick_labels=month_names,
                patch_artist=True,
                medianprops=dict(color=dCols["text"], linewidth=2.0),
                whiskerprops=dict(color=dCols["text"]),
                capprops=dict(color=dCols["text"]),
                boxprops=dict(edgecolor=dCols["text"]),
                flierprops=dict(marker=".", markersize=3,
                                markerfacecolor=dCols["text"], alpha=0.4))
for patch, mean_val in zip(bp["boxes"], monthly_tmax_mean):
    patch.set_facecolor(cmap(norm(mean_val)))
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
fig.colorbar(sm, ax=ax, label="Mean Tmax (°C)")
ax.set_xlabel("Month")
ax.set_ylabel("Max temperature (°C)")
ax.set_title("Box Plot — Tmax by month")
ax.tick_params(axis="x", rotation=45)
tidy(ax)
fig.tight_layout()
fig.savefig("plot_boxplot.pdf", **SAVE)
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
vp["cmedians"].set_color(dCols["struct"])
vp["cmedians"].set_linewidth(2.0)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names, rotation=45, ha="right")
ax.set_xlabel("Month")
ax.set_ylabel("Max temperature (°C)")
ax.set_title("Violin Plot — Tmax by month")
tidy(ax)
fig.tight_layout()
fig.savefig("plot_violin.pdf", **SAVE)
plt.close()

# ================================================================
# 7 — Error bars & ribbon
# ================================================================
x = np.arange(1, 13)

fig, ax = plt.subplots(**FIG)
ax.fill_between(x,
                monthly_mean - monthly_std,
                monthly_mean + monthly_std,
                alpha=0.25, color=dCols["alert"], label="±1 SD")
ax.plot(x, monthly_mean,
        color=dCols["alert"], linewidth=1.5, label="Monthly mean")
ax.errorbar(x, monthly_mean, yerr=monthly_std,
            fmt="none", capsize=4,
            color=dCols["struct"], linewidth=1.0)
ax.set_xticks(x)
ax.set_xticklabels(month_names, rotation=45, ha="right")
ax.set_xlabel("Month")
ax.set_ylabel("Mean temperature (°C)")
ax.set_title("Error Bars & Ribbon — monthly mean ± 1 SD")
ax.legend(frameon=False)
tidy(ax)
fig.tight_layout()
fig.savefig("plot_errorbars.pdf", **SAVE)
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
ax.set_title("Heatmap — mean Tmax by month and year")
fig.tight_layout()
fig.savefig("plot_heatmap.pdf", **SAVE)
plt.close()
