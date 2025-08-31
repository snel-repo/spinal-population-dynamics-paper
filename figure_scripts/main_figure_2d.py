# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sd_path = "../data/SourceData.xlsx"

C_ID = 1 
cname = f"c{C_ID}"
# %% [ SOURCE DATA PLOT - MAIN FIGURE 2D ]
df_all = pd.read_excel(sd_path, sheet_name=f"Fig2D_{cname}", header=None)

fig = plt.figure(figsize=(1.5,2.5), dpi=300)
ax = fig.add_subplot(111)

x = df_all.iloc[1:,0].astype(float) # cycle durations
y = df_all.iloc[1:,1].astype(float) # avg. neural speeds

ax.scatter(x, y, s=2, color="k")
bf_curve = np.poly1d(np.polyfit(x,y,1)) # fit best fit line
ax.plot(np.unique(x), bf_curve(np.unique(x)), color="k", linewidth=1)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set_xlabel("Cycle duration (ms)", fontsize=fs)
ax.set_ylabel("Avg. neural speed (a.u.)", fontsize=fs)

fs = 10
tick_fs = 8
xmin = 550
xmax = 1250
x_pos = xmin

if cname == "c1":        
    y_pos_offset = 0.05
    ymin = 0.6    
    ymax = 1.8
elif cname == "c2":    
    y_pos_offset = 0.02
    ymin = 0.4
    ymax = 1.3

y_pos = ymin + y_pos_offset
ax.text(x_pos,y_pos, f"r={np.corrcoef(x, y)[0,1]:.2f}", va="bottom", fontsize=fs)
ax.set_ylim([ymin, ymax])
ax.set_xlim([xmin, xmax])
ax.set_yticks(np.round(np.arange(ymin, ymax+0.1, 0.2),1))

#y-axis
twinx = ax.twinx()
twinx.spines["left"].set_position(("axes", -0.1))
twinx.yaxis.tick_left()
twinx.yaxis.set_label_position("left")
twinx.yaxis.set_ticks_position("left")
twinx.tick_params(axis="both", which="major", labelsize=tick_fs, pad=0, tickdir="out")
twinx.set_ylim(ax.get_ylim())
twinx.set_yticks(ax.get_yticks())
twinx.set_yticklabels(twinx.get_yticks())
twinx.spines["top"].set_visible(False)
twinx.spines["right"].set_visible(False)
twinx.set_ylabel("Avg. neural speed (a.u.)", fontsize=fs)
ax.spines["left"].set_visible(False)
ax.yaxis.set_visible(False)

plt.show()