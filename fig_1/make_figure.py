import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
from matplotlib.patches import ConnectionPatch, Rectangle
from scipy.interpolate import CubicSpline

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 5,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.4,
    "ytick.major.width": 0.4,
    "xtick.major.size": 1.5,
    "ytick.major.size": 1.5,
})

# ---- sizes in points (the figure is 216 x 216 pt = 3 x 3 in) ----
W = 216
H_A, H_B = 106.71, 61.5              # native heights of panelA.png / panelB.png
H_C = W - H_A - H_B                  # whatever is left goes to panel C
ZOOM_X_PT = (183.21, 185.78)         # 443-490 Ma box in panel B (pt from left edge)
ZOOM_Y_PT = 53.0                     # bottom of that box (pt from top of panel B)

imgA = plt.imread("panelA.png")
imgB = plt.imread("panelB.png")
df = pd.read_csv("tl_cartoon.csv").sort_values("age_Ma")
pts = pd.read_csv("tl_ostrander2025_digitized.csv")

fig = plt.figure(figsize=(3, 3))
gs = gridspec.GridSpec(3, 1, figure=fig, height_ratios=[H_A, H_B, H_C],
                       left=0, right=1, top=1, bottom=0, hspace=0)

# ---- Panels A and B: images, no axes ----
axA = fig.add_subplot(gs[0])
axB = fig.add_subplot(gs[1])
for ax, img in ((axA, imgA), (axB, imgB)):
    ax.imshow(img, interpolation="lanczos")
    ax.set_axis_off()
    ax.set_aspect("auto")   # the gridspec rows already match the image aspect

# ---- Panel C: Tl cartoon (plot row + period bar), margins in pt ----
gsC = gs[2].subgridspec(4, 3, height_ratios=[4, H_C - 15.7, 5.2, 6.5],
                        width_ratios=[46, W - 46 - 6, 6], hspace=0, wspace=0)
axC = fig.add_subplot(gsC[1, 1])
axP = fig.add_subplot(gsC[2, 1], sharex=axC)

age = np.linspace(df.age_Ma.min(), df.age_Ma.max(), 400)
spl = CubicSpline(df.age_Ma, df.eps205Tl_auth, bc_type="natural")
eps = spl(age)
hw = np.interp(age, df.age_Ma, df.envelope_halfwidth)
purple = "#6B3FA0"
axC.scatter(pts.age_Ma, pts.eps205Tl_auth, s=2.2, facecolor="#BDBDBD",
            edgecolor="#8A8A8A", linewidth=0.15, zorder=1, clip_on=True)
axC.fill_between(age, eps - hw, eps + hw, color=purple, alpha=0.18, lw=0, zorder=2)
axC.plot(age, eps, color=purple, lw=1.1, solid_capstyle="round", zorder=3)

axC.set_xlim(490, 450)               # older on the left, like panel B
axC.set_ylim(-5.4, 1.0)
axC.set_yticks([-4, -2, 0])
axC.set_yticklabels(["−4", "−2", "0"])
axC.set_ylabel(r"$\varepsilon^{205}$Tl$_{\mathrm{auth}}$", fontsize=5.6, labelpad=1.5)
axC.set_xticks([485, 475, 465, 455])
axC.tick_params(axis="x", direction="in", labelbottom=False)
axC.tick_params(axis="y", pad=1)

axC.annotate("", xy=(487.6, -5.3), xytext=(487.6, -3.6),
             arrowprops=dict(arrowstyle="-|>", lw=0.45, color="#231f20",
                             mutation_scale=4, shrinkA=0, shrinkB=0))
axC.text(487.0, -4.95, "more oxygenated deep water", fontsize=4.4,
         style="italic", va="center")

# period bar
for a0, a1, name, col, tc in [(490, 486.85, "Cm", "#7FA056", "#231f20"),
                              (486.85, 443.07, "Ordovician", "#009270", "#ffffff")]:
    axP.add_patch(Rectangle((a1, 0), a0 - a1, 1, facecolor=col,
                            edgecolor="#231f20", lw=0.3))
    axP.text((a0 + a1) / 2, 0.5, name, ha="center", va="center",
             fontsize=4.4, fontweight="bold", color=tc)
axP.set_ylim(0, 1)
for sp in axP.spines.values():
    sp.set_visible(False)
axP.set_yticks([])
axP.tick_params(axis="x", length=1.2, pad=0.8, labelsize=4.4)
axP.set_xticks([485, 475, 465, 455])
axP.set_xticklabels(["485", "475", "465", "455 Ma"])

# ---- zoom connectors from the box in B to panel C ----
sx = imgB.shape[1] / W               # pixels per pt in panelB.png
for x_pt, corner in ((ZOOM_X_PT[0], (0, 1)), (ZOOM_X_PT[1], (1, 1))):
    # box is drawn with present on the right: left edge = 490 Ma, right edge = 443 Ma
    con = ConnectionPatch(xyA=(x_pt * sx, ZOOM_Y_PT * sx), coordsA=axB.transData,
                          xyB=corner, coordsB=axC.transAxes,
                          lw=0.3, ls=(0, (2.5, 2)), color="#231f20")
    fig.add_artist(con)

# ---- panel letters ----
for y_pt, letter in ((0, "A"), (H_A + 1, "B"), (H_A + H_B + 1, "C")):
    fig.text(1.5 / W, 1 - (y_pt + 7) / W, letter, fontsize=8, fontweight="bold")

fig.savefig("Fig1.pdf")
fig.savefig("Fig1.png", dpi=600)
plt.show()
