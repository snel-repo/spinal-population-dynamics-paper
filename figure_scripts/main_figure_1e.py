# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sd_path = "../data/SourceData.xlsx"

C_ID = 2 
cname = f"c{C_ID}"

# %% [ SOURCE DATA PLOT - MAIN FIG 1E ]
df_all = pd.read_excel(sd_path, sheet_name=f"Fig1E_{cname}", header=0)

spk_vals = df_all.spk_var_expl
emg_vals = df_all.emg_var_expl

emg_vals = emg_vals[~pd.isna(emg_vals)]

bins = np.arange(0,1.1,0.05)
opacity = 0.9
tick_fs = 8
fs = 10
spine_lw = 1

fig = plt.figure(figsize=(2,1.7), dpi=300)
ax = fig.add_subplot(111)
spk_color = "gray"
emg_color = "mediumaquamarine"
edge_color = "black"
edge_width = 0.1
ax.hist(spk_vals.values, 
        alpha=opacity, 
        facecolor=spk_color,  
        edgecolor=edge_color,
        linewidth=edge_width,                
        bins=bins, 
        label="EMG -> Spikes (cross)"
        )



ax.hist(emg_vals.values, 
        alpha=opacity, 
        facecolor=emg_color, 
        edgecolor=edge_color,
        linewidth=edge_width,        
        bins=bins, 
) 

ax.set_xlim([0,1.0])
y_lim = 40# 60, woody
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(spine_lw)
ax.spines["bottom"].set_linewidth(spine_lw)
ax.tick_params(axis='both', which='major', labelsize=tick_fs, tickdir="out")
ax.tick_params(axis='both', which='minor', labelsize=tick_fs)
ax.tick_params(width=spine_lw)
ax.set_ylim([0, y_lim])
ax.set_yticks(ax.get_yticks()[1:])
ax.set_xticks(np.arange(0,1.1,0.2))
ax.set_ylabel("counts", fontsize=fs, labelpad=-0.8)
ax.set_xlabel("Var. explained", fontsize=fs, labelpad=1.5)

# y-axis
twinx = ax.twinx()
twinx.spines["left"].set_position(("axes", -0.1))
twinx.yaxis.tick_left()
twinx.yaxis.set_label_position("left")
twinx.yaxis.set_ticks_position("left")
twinx.tick_params(axis="both", which="major", labelsize=tick_fs, pad=0, tickdir="out")
twinx.set_ylim([0, y_lim])
twinx.spines["top"].set_visible(False)
twinx.spines["right"].set_visible(False)
twinx.set_ylabel(f"Counts", fontsize=fs)

ax.yaxis.set_visible(False)
ax.spines["left"].set_visible(False)

fig.tight_layout()

plt.show()