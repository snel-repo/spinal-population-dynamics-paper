# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as colormap
import colorcet as cc

C_ID = 1 
cname = f"c{C_ID}"

sd_path = "../data/SourceData.xlsx"
# %% [ SOURCE DATA PLOT: MAIN FIGURE 4A]
tick_fs = 8
BIN_SIZE = 10
MARGIN_MS = 150

if cname == "c1":
    MIN_MAG = 6.416
    MAX_MAG = 20.269
elif cname == "c2":
    MIN_MAG = 6.416
    MAX_MAG = 20.269


df_all = pd.read_excel(sd_path, sheet_name=f"Fig4A_{cname}", header=None)

block_width = 12

musc_name = "RBA"
start_col = df_all.iloc[0][df_all.iloc[0,:] == musc_name].index[0]
end_col = start_col + block_width

t_vec = df_all.iloc[4:-2,0]
cond_avgs = df_all.iloc[4:-2,start_col:end_col:2]
cond_sems = df_all.iloc[4:-2,start_col+1:end_col+1:2]
c_vals = df_all.iloc[-1, start_col:start_col+12:2]
assert cond_avgs.shape[1] == cond_sems.shape[1], 'Error: must have a corresponding sem or each avg'
n_conds = cond_avgs.shape[1]
fig = plt.figure(figsize=(2.0,1.75), dpi=300) # EMG Magnitude PSTH

ax = fig.add_subplot(111)
plot_scale_label = True
plot_text_label = True
alpha = 1.0
fs = 10
lw = 1.0 # 1.5 for spikes, 2.5 for EMG, 2 for PCs
cm = cc.m_kbc
unit_str = "$\mu$V"

if plot_scale_label:
    scale_color ="black"        
else:
    scale_color = "white"

if cname == "c1":
    ylim_max = 40
    ybar_height = 10
    xbar_label_offset = 3.4
    xbar_offset = -0.55
    ylim_offset = -2.0
if cname == "c2":
    ylim_max = 140
    ybar_height = 50 
    xbar_label_offset = 12.0
    xbar_offset = -2.75
    ylim_offset = -3.4

ybar_min = 0.01
ybar_name = f"{ybar_height:.0f} {unit_str}"
ybar_offset = 25 # 20 for spikes, 30 for EMG/PCs
ylim_min = ybar_min + xbar_offset + ylim_offset


for i in range(n_conds):
    cond_avg = cond_avgs.iloc[:,i]  # condition average
    cond_sem = cond_sems.iloc[:,i]  # std. error of mean
    c_val = c_vals.iloc[i]               # color value
    dat_mask = ~cond_avg.isna()     # mask nans
    ca = cond_avg[dat_mask].values.astype(float)  # apply mask to data and time vec
    cs = cond_sem[dat_mask].values.astype(float)
    t_vec_ms = t_vec[dat_mask].values.astype(int) 
    color = cm(c_val)               # pick color        
    ax.plot(t_vec_ms, ca,           # plot cond. avg
            color=color, alpha=alpha, 
            linewidth=lw) 
    ax.fill_between(t_vec_ms,       # plot sem
                    ca-cs, ca+cs,                     
                    color=color,
                    alpha=0.1) 

# -- scale bar for time (horizontal)
xbar_min = ybar_min + xbar_offset
time_scale_bar_len_ms = 100 # ms
time_scale_bar_len = int(time_scale_bar_len_ms/BIN_SIZE)
ax.plot([t_vec_ms[0], t_vec_ms[time_scale_bar_len]], [xbar_min, xbar_min], linewidth=lw, color="k")
if plot_text_label:
    ax.text(t_vec_ms[int(time_scale_bar_len/2.0)], xbar_min-xbar_label_offset, s=f"{time_scale_bar_len_ms}ms", ha="center", fontsize=tick_fs)

# -- scale bar for magnitude (vertical)
ax.plot([t_vec_ms[0]-ybar_offset, t_vec_ms[0]-ybar_offset], [ybar_min, ybar_min + ybar_height], linewidth=lw, color="k")

# -- extensor burst onset point
ms = 4 
ax.plot(t_vec_ms[np.round(MARGIN_MS/BIN_SIZE).astype(int)], xbar_min, 'o', color="g", markersize=ms, mec="black", mew=0.5)    
# --- state space marker
ax.plot(t_vec_ms[np.round((MARGIN_MS+200)/BIN_SIZE).astype(int)], xbar_min, 'o', color="darkorange", mec="black", mew=0.5, markersize=ms)
# -- text for scale bar
scale = 4.0
ax.text(t_vec_ms[0]-(ybar_offset*scale), ybar_min + ybar_height*0.34, s=f"{ybar_height} {unit_str}", rotation=90, fontsize=fs, color=scale_color)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_visible(False)

ax.set_xlim([-200, 350])

norm = matplotlib.colors.Normalize(vmin=MIN_MAG, vmax=MAX_MAG)
cbar = fig.colorbar(colormap.ScalarMappable(norm=norm, cmap=cm), ax=ax, orientation="vertical", shrink=0.85, pad=-0.03)
cbar.set_label(f"Peak burst mag. ({unit_str})", fontsize=fs-1)
cbar.ax.set_yticklabels(cbar.ax.get_yticks().astype(int), fontsize=fs-2)
cbar.ax.yaxis.set_tick_params(pad=-0.5, length=2)
cbar.outline.set_visible(False)
ax.set_ylim([ylim_min, ylim_max])
ax.yaxis.set_visible(False)
ax.xaxis.set_visible(False)
fig.tight_layout()

plt.show()