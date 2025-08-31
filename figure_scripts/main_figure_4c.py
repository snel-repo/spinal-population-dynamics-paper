# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sd_path = "../data/SourceData.xlsx"

C_ID = 1 
cname = f"c{C_ID}"

df_all = pd.read_excel(sd_path, sheet_name=f"Fig4C_{cname}", header=0)
# quanitfication plot
fig = plt.figure(figsize=(2,2), dpi=300)
ax = fig.add_subplot(111)

fs = 10
tick_fs = 8
fit_lw = 1
unit_str = "$\mu$V"

if cname == "c1":
    mag_min = -2
    mag_max = 27
    ss_min = 1.5 
    ss_max =  6.5 
    txt_x_pos = 1.5 
    txt_y_pos = 0
    ylab_space = 5
    xlab_space = 2
    xlab_start_offset = 0
    xlab_stop_offset = 1
elif cname == "c2":        
    mag_min = -10
    mag_max = 95    
    ss_min = -2
    ss_max = 5
    ylab_space = 25
    xlab_space = 4
    xlab_start_offset = 1
    xlab_stop_offset = 2
    txt_x_pos = ss_min
    txt_y_pos = -5
    
x = df_all.ss_pos
y = df_all.emg_mag

# for plotting line
bf_curve = np.poly1d(np.polyfit(x,y,1)) # fit best fit line

# for computing predictive model of magnitude
# compute avg. error
mag_pred = bf_curve(x)
abs_pred_error = np.abs(y - mag_pred)
median_abs_error = np.round(np.median(abs_pred_error),2)
ax.scatter(x, y, s=2, color='k')
ax.plot(np.unique(x), bf_curve(np.unique(x)), color="k", linewidth=fit_lw)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_xlabel("State space pos. (a.u.)", fontsize=fs, labelpad=0.5)
r_val = np.corrcoef(x, y)[0,1]
n_cycles = x.size
    
ax.set_ylim([mag_min, mag_max])
ax.set_xlim([ss_min, ss_max])
ax.set_xticks(np.round(np.arange(ss_min+xlab_start_offset, ss_max+xlab_stop_offset, xlab_space),1))
ax.set_xticklabels(ax.get_xticks(), fontsize=tick_fs)
ax.set_yticks(np.arange(0, mag_max+1, ylab_space).astype(int))
ax.set_yticklabels(ax.get_yticks(), fontsize=tick_fs)

ax.text(txt_x_pos, txt_y_pos, f"$r$ = {r_val:.2f}\nMAE: {median_abs_error}$\mu$V", fontsize=tick_fs)
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
twinx.set_ylabel(f"Peak EMG mag. ({unit_str})", fontsize=fs)

ax.spines["left"].set_visible(False)
ax.yaxis.set_visible(False)
#ax.set_ylim([-1, 1])
fig.tight_layout()

plt.show()