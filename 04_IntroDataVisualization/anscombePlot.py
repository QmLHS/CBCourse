import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('lecturesOliveFluo')


# cyan glow                   `#0FFFFF`
# light cyan                  `#D9F7F4`
# ice blue                    `#99FFFF`
# aquamarine                  `#7FFFD4`
# metallic seaweed            `#028090`
# outer space                 `#474747`
# bright green                `#66FF00`
# lemon lime                  `#E3FF00`
# arctic lime                 `#D0FF14`
# ocean mint                  `#3AB09E`
# midnight green eagle green  `#114B5F`
# midnight green              `#004953`
# black olive                 `#3B3C36`
# bone                        `#CFD4C5`
# cream                       `#FFFFD7`
# bistre                      `#3D2B1F`
# raspberry                   `#E30B5C`
# coral                       `#F88379`
# cherry blossom pink         `#FFB7C5`
# myOrange                    `#FF7F00` 
# gold                        `#FFD700`
# maize                       `#FBEC5D`


# * **background** black olive
# * **text** bone
# * **structure** arctic lime
# * **alert** aquamarine
# * **example** gold


dCols = {
    "text":  "#CFD4C5",
    "bg": "#3B3C36",
    "struct": "#D0FF14",
    "alert": "#7FFFD4",
    "example": "#FFD700",
    "red": "#F88379"
}

quartet = pd.read_csv("anscombe1973.csv", comment="#")

datasets = ["I", "II", "III", "IV"]

fig, axes = plt.subplots(1, 4, figsize=(16, 4), sharex=False, sharey=False)

for ax, label in zip(axes.flat, datasets):
    subset = quartet[quartet["dataset"] == label]
    x, y   = subset["x"].values, subset["y"].values

    ax.scatter(x, y, color=dCols["struct"], s=40, zorder=3)

    # least-squares regression line
    m, b  = np.polyfit(x, y, deg=1)
    x_fit = np.linspace(x.min(), x.max(), 100)
    ax.plot(x_fit, m * x_fit + b, color=dCols["red"], linewidth=1.2)

    ax.set_title(f"Dataset {label}", fontweight="bold")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xlim(0, 22)
    ax.set_ylim(2, 14)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # per-panel stats
    ax.text(0.05, 0.95,
            f"$\\bar{{x}}={x.mean():.1f}$  $\\bar{{y}}={y.mean():.2f}$\n"
            f"$r={np.corrcoef(x, y)[0,1]:.3f}$",
            transform=ax.transAxes,
            va="top", fontsize=8, color="0.4")

fig.suptitle("Anscombe's Quartet (1973)", fontsize=13, fontweight="bold")
fig.tight_layout()
fig.savefig("anscombeQuartetPlot.pdf", bbox_inches="tight")
