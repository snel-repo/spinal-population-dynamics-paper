# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sd_path = "../data/SourceData.xlsx"

C_ID = 2 
cname = f"c{C_ID}"

# %% [ SOURCE DATA PLOT - MAIN FIG 1D ]

df_all = pd.read_excel(sd_path, sheet_name=f"Fig1D_{cname}", header=0)

r2_mean = df_all.norm_r2_mean.values
r2_sem = df_all.norm_r2_sem.values
num_pcs = r2_mean.shape[0]

fs = 10
tick_fs = 8 
opacity = 0.7
lw = 1
dash_lw = 0.8
spine_lw = 1
ms = 5
cross_ixs = [1, 6]

fig = plt.figure(figsize=(1.8, 1.7), dpi=300)
ax =fig.add_subplot(111)

lin = ax.plot(np.arange(1,num_pcs+1), r2_mean[:num_pcs], '-o', color="k", linewidth=lw, markersize=ms)
lin[0].set_clip_on(False)
#ax.fill_between(np.arange(1, r2_mean.size+1), r2_mean-r2_sem, r2_mean+r2_sem, color='k', alpha=0.2)
ax.fill_between(np.arange(1, num_pcs+1), r2_mean[:num_pcs]-r2_sem[:num_pcs], r2_mean[:num_pcs]+r2_sem[:num_pcs], color='k', alpha=0.2)
ax.set_ylim([0, 1.1])
ax.set_xlim([0.5, num_pcs+1])
for cross_ix in cross_ixs:
    hlin = ax.hlines(r2_mean[cross_ix], xmin=0.5, xmax=cross_ix+1, color="k", linestyle="--", linewidth=dash_lw, alpha=opacity)
    hlin.set_clip_on(False)
    vlin = ax.vlines(cross_ix+1, ymin=0, ymax=r2_mean[cross_ix], color="k", linestyle="--", linewidth=dash_lw, alpha=opacity)
    vlin.set_clip_on(False)
    ax.text(0.45, r2_mean[cross_ix]*1.03, f"{r2_mean[cross_ix]:.2f}", fontsize=tick_fs-1, ha="left", va="bottom", alpha=opacity)
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(spine_lw)
ax.spines["bottom"].set_linewidth(spine_lw)
ax.tick_params(width=spine_lw, length=4)

ax.set_xlabel("# of PCs", fontsize=fs, labelpad=-0.1)

ax.set_ylim([0, 1.0])
ax.set_xlim([1, 7])
ax.set_xticks(np.arange(1, num_pcs+1, 2))
ax.set_yticks([0, 1])
#ax.yaxis.set_visible(False)

# y-axis
twinx = ax.twinx()
twinx.spines["left"].set_position(("axes", -0.1))
twinx.yaxis.tick_left()
twinx.yaxis.set_label_position("left")
twinx.yaxis.set_ticks_position("left")
twinx.tick_params(axis="both", which="major", labelsize=tick_fs, pad=0, tickdir="out")
twinx.set_ylim([0, 1.0])
twinx.set_yticks(np.arange(0,1.1,0.2))
twinx.spines["top"].set_visible(False)
twinx.spines["right"].set_visible(False)
twinx.set_ylabel("Norm. decoding $R^2$", fontsize=fs)
#twinx.set_ylabel(f"var. explained", fontsize=fs)

ax.yaxis.set_visible(False)
ax.spines["left"].set_visible(False)

ax.tick_params(axis="both", which="major", labelsize=tick_fs, pad=2, tickdir="out")
ax.tick_params(axis="both", which="minor", labelsize=tick_fs, pad=2)
fig.tight_layout(pad=1.0)

plt.show()