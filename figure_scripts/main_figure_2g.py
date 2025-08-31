# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as colormap

sd_path = "../data/SourceData.xlsx"

C_ID = 1
cname = f"c{C_ID}"

# %% === [ SOURCE DATA PLOT - MAIN FIGURE 2G ]
df_all = pd.read_excel(sd_path, sheet_name=f"Fig2G_{cname}", header=None)

cm = colormap.Blues
mark_size = 5
tick_fs = 8
fs = 10
fit_lw = 1
xmin = -100
ymin = 150
ymax = 850

fig = plt.figure(figsize=(3.75,2.75), dpi=150)
ax = fig.add_subplot(111)

crossing_names = df_all.iloc[:, ::-1].iloc[0,1:-1].values.tolist()
plane_crossings = df_all.iloc[:, ::-1].iloc[1:,1:-1]
bur_dur = df_all.iloc[1:,0]
spinal_osc_exit = df_all.iloc[1:,-1]
color_list = []
for j in range(len(crossing_names)):
    color = cm((j+1)/(len(crossing_names)+2))
    color_list.append(color)

for i, color in enumerate(reversed(color_list)):
    plane_tx = plane_crossings.iloc[:,i]       
    x = plane_tx
    y = bur_dur     
    ax.scatter(x, y, color=color, s=mark_size, edgecolor='k', linewidth=0.3, alpha=0.8)    
        
x = spinal_osc_exit.values.astype(float)
y = bur_dur.values.astype(float)
ax.scatter(x, y, s=mark_size, color="limegreen", edgecolor="k", linewidth=0.5, alpha=0.8)
bf_curve = np.poly1d(np.polyfit(x,y,1)) # fit best fit line
# compute avg. error
burst_pred = bf_curve(x)

pred_error = np.abs(bur_dur - burst_pred)
median_abs_error = np.round(np.median(pred_error),1)
n_cycles = x.size

r_val = np.round(np.corrcoef(x,y)[0,1],2)
ax.plot(np.unique(x), bf_curve(np.unique(x)), color="k", linewidth=fit_lw)
ax.text(850, 190, f"$r$={r_val}\nMAE={median_abs_error} ms", va="bottom", ha="right", fontsize=tick_fs)

ax.set_xlim([xmin, ymax])
ax.set_ylim([ymin, ymax])
ax.set_xticks(np.arange(0, 1000, 200).astype(int))
ax.set_yticks(np.arange(200, 1000, 200).astype(int))
ax.set_xticklabels(ax.get_xticks().astype(int), fontsize=tick_fs)
ax.set_yticklabels(ax.get_yticks().astype(int), fontsize=tick_fs)
ax.set_ylabel("Extensor burst offset (ms)", fontsize=fs)
ax.set_xlabel("Spinal state space crossing (ms)", fontsize=fs)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# y-axis
twinx = ax.twinx()
twinx.spines["left"].set_position(("axes", -0.05))
twinx.yaxis.tick_left()
twinx.yaxis.set_label_position("left")
twinx.yaxis.set_ticks_position("left")
twinx.tick_params(axis="both", which="major", labelsize=tick_fs, pad=0, tickdir="out")
twinx.set_ylim(ax.get_ylim())
twinx.set_yticks(ax.get_yticks())
twinx.set_yticklabels(twinx.get_yticks(), fontsize=tick_fs)
twinx.spines["top"].set_visible(False)
twinx.spines["right"].set_visible(False)
twinx.set_ylabel(f"Extensor burst offset (ms)", fontsize=fs)

ax.yaxis.set_visible(False)
ax.spines["left"].set_visible(False)

plt.show()