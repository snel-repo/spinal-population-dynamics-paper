# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import colorcet as cc

sd_path = "../data/SourceData.xlsx"
# %% [ SOURCE DATA PLOT - MAIN FIGURE 2C ]
df_all = pd.read_excel(sd_path, sheet_name="Fig2C", header=None)
tick_fs = 8
BIN_SIZE = 10
MARGIN_MS = 150
MIN_BURST_DUR_MS = 180
MAX_BURST_DUR_MS = 800

fig = plt.figure(figsize=(1.5,1.5), dpi=300) # Spinal neuron PSTH
ax = fig.add_subplot(111)

unit_id = 0

unit_name = f"unit_{unit_id}"
block_width = 12

start_col = df_all.iloc[0][df_all.iloc[0,:] == unit_name].index[0]
end_col = start_col + block_width

t_vec = df_all.iloc[4:-2,0]
cond_avgs = df_all.iloc[4:-2,start_col:end_col:2]
cond_sems = df_all.iloc[4:-2,start_col+1:end_col+1:2]
c_vals = df_all.iloc[-1, start_col:start_col+12:2]
assert cond_avgs.shape[1] == cond_sems.shape[1], 'Error: must have a corresponding sem or each avg'
n_conds = cond_avgs.shape[1]

plot_scale_label = True
plot_text_label = False

alpha = 1.0
fs = 10
lw = 1.0 # 1.5 for spikes, 2.5 for EMG, 2 for PCs

cm = cc.m_bmy

if plot_scale_label:
    scale_color ="black"        
else:
    scale_color = "white"

xbar_label_offset = 5
xbar_offset = -0.55 # -0.5 for spikes, -0.7 for PCs, -0.02 for EMG


ylim_offset = -2.0
ybar_min = 0.01
ybar_height = 10 # spks/s
ybar_offset = 35
xbar_offset = -1.5 #-1.5
ylim_offset = -2.0
ylim_min = ybar_min + xbar_offset + ylim_offset
ylim_max = 40 #0.30

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

# -- text for scale bar
scale = 5.0
ax.text(t_vec_ms[0]-(ybar_offset*scale), ybar_min + ybar_height*0.34, s=f"{ybar_height} spk/s", rotation=90, fontsize=fs, color=scale_color)

# -- axis formatting
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.yaxis.set_visible(False)
ax.xaxis.set_visible(False)
ax.set_xlim([-200, 850])
fig.tight_layout()

plt.show()