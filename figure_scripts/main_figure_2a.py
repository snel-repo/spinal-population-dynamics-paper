# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import colorcet as cc

sd_path = "../data/SourceData.xlsx"
# %% [ SOURCE DATA PLOT - MAIN FIGURE 2A ]
df_all = pd.read_excel(sd_path, sheet_name=f"Fig2A", header=0)

n_cycles = df_all.shape[1] - 1

end_ix = df_all.iloc[0, 1:].astype(int)
c_val = df_all.iloc[1, 1:]
bur_dur = df_all.iloc[2, 1:].astype(int)

t_vec_ms = df_all.iloc[4:, 0].astype(int)
dat_mat = df_all.iloc[4:, 1:]

fig = plt.figure(figsize=(2.25,3.25), dpi=300)
ax = fig.add_subplot(111)
ax.spines["top"].set_visible(False) 
ax.spines["right"].set_visible(False)

spacing = 0.2
scaling = 0.05
lw = 0.5 # 1
ms = 1 # 3
fs = 10 # 20
tick_fs = 8 # 16

cm = cc.m_bmy


for i in range(n_cycles):            
    c = cm(c_val.iloc[i])
    bdur = bur_dur.iloc[i]
    e_ix = end_ix.iloc[i]
    dat_cyc = dat_mat.iloc[:, i]
    dat_mask = ~dat_cyc.isna()
    t_vec = t_vec_ms[dat_mask]
    dat = dat_cyc[dat_mask]    
    ax.plot(t_vec, dat[dat_mask]+(i*spacing)*scaling, linewidth=lw, color="k", alpha=0.2)
    ax.plot([t_vec.iloc[e_ix]], [dat.iloc[e_ix]+(i*spacing)*scaling], 'o', color="r", alpha=0.6, markersize=ms)    
    ax.plot([t_vec.iloc[0]], [dat.iloc[0]+(i*spacing)*scaling], 's', color=c, alpha=0.6, markersize=ms+2)    
    if i == 0 or i == n_cycles-1:
        ax.text(t_vec.iloc[0]-400,
                dat.iloc[0]+(i*spacing)*scaling,
                s=f"{int(bdur)} ms",
                fontsize=tick_fs
        )

# vertical green line denoting alignment point
ax.vlines(x=0, ymin=0, ymax=(dat+(i*spacing)*scaling).max(),
        linestyle="--",
        color="g",
)

ax.yaxis.set_visible(False)
ax.xaxis.set_visible(False)
yoffset = -0.1
ax.plot([-150, -50], [yoffset, yoffset], linewidth=2, color="k")

ax.text(-150, yoffset-0.3, s="100ms", fontsize=tick_fs, color="k", ha="left")
ax.set_xlabel("Time rel. to ext. burst onset", fontsize=fs)
ax.set_xlim(-150, 950)
ax.set_xticklabels(np.round(ax.get_xticks()).astype(int), fontsize=tick_fs)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.tick_params(width=2)
fig.tight_layout()

plt.show()