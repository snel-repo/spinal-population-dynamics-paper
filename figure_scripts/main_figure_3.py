# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from utils.utils import draw_error_band

sd_path = "../data/SourceData.xlsx"

# %% [ SOURCE DATA PLOT - MAIN FIGURE 3 ]

del_id = 3 # 1, 2, or 3

assert del_id > 0 and del_id < 4, 'Must select del_id= 1, 2, or 3'
dname = f"deletion_{del_id}"

traj_lw = 0.75
trace_offset = -0.6
plot_extra_labels = False
# scale bar parameters
corner = -8
length = 3.5
lab_offset = -2.7
xlab_offset = 0.5
ylab_offset = 0.8

c1 = matplotlib.colors.to_rgba("dodgerblue") #"mediumblue"
c2 = matplotlib.colors.to_rgba("tomato") # "orangered"
c3 = "black" # "forestgreen"
fs = 10 
# draw extensor/flexion regions
c1_alpha = list(c1)
c2_alpha = list(c2)
shade_alpha = 0.7
c1_alpha[3] = shade_alpha
c2_alpha[3] = shade_alpha
err = 1.5



df_all = pd.read_excel(sd_path, sheet_name="Fig3", header=None)
col0 = df_all.iloc[0][df_all.iloc[0,:] == dname].index[0]
block_width = 14
coln = col0 + block_width

del_start_ix = df_all.iloc[1,col0+1]
del_end_ix = df_all.iloc[2,col0+1]
t_vec = df_all.iloc[6:,col0+1].values
dat = df_all.iloc[6:,col0+2:col0+4].values
dat_ext = df_all.iloc[6:,col0+5:col0+6].values
dat_flx = df_all.iloc[6:,col0+7:col0+8].values

ext_hull = df_all.iloc[6:,col0+9:col0+11]
ext_hull = ext_hull.loc[~pd.isna(ext_hull.iloc[:,0]),:].astype(float).values
flx_hull = df_all.iloc[6:,col0+12:col0+14]
flx_hull = flx_hull.loc[~pd.isna(flx_hull.iloc[:,0]),:].astype(float).values

fig = plt.figure(figsize=(8,2), dpi=150)

ax1 = fig.add_subplot(142)
ax2 = fig.add_subplot(143)
ax3 = fig.add_subplot(144)
ax4 = fig.add_subplot(141)

ax1.plot(dat[:del_start_ix,0], dat[:del_start_ix,1], zorder=1, color=c3, linewidth=traj_lw)
ax2.plot(dat[del_start_ix-1:del_end_ix,0], dat[del_start_ix-1:del_end_ix,1], zorder=1, color=c3, linewidth=traj_lw)
ax3.plot(dat[del_end_ix-1:,0], dat[del_end_ix-1:,1], zorder=2, color=c3, linewidth=traj_lw)


draw_error_band(ax1, ext_hull[:,0], ext_hull[:,1], err, facecolor=c1_alpha, edgecolor=(0,0,0,0), zorder=1)
draw_error_band(ax1, flx_hull[:,0], flx_hull[:,1], err, facecolor=c2_alpha, edgecolor=(0,0,0,0), zorder=1)
#draw_error_band(ax1, dat_3d[first_ext_onset:first_ext_offset,0], dat_3d[first_ext_onset:first_ext_offset,1], err, facecolor=c1_alpha, edgecolor=(0,0,0,0), zorder=1)
#draw_error_band(ax1, dat_3d[first_ext_offset-1:second_ext_onset-1,0], dat_3d[first_ext_offset-1:second_ext_onset-1,1], err, facecolor=c2_alpha, edgecolor=(0,0,0,0), zorder=1)

draw_error_band(ax2, ext_hull[:,0], ext_hull[:,1], err, facecolor=c1_alpha, edgecolor=(0,0,0,0), zorder=1)
draw_error_band(ax2, flx_hull[:,0], flx_hull[:,1], err, facecolor=c2_alpha, edgecolor=(0,0,0,0), zorder=1)

draw_error_band(ax3, ext_hull[:,0], ext_hull[:,1], err, facecolor=c1_alpha, edgecolor=(0,0,0,0), zorder=1)
draw_error_band(ax3, flx_hull[:,0], flx_hull[:,1], err, facecolor=c2_alpha, edgecolor=(0,0,0,0), zorder=1)


# extensor
trace_col_ext = "black"
trace_col_flx = "gray"
ax4.plot(t_vec[:del_start_ix], dat_ext[:del_start_ix], color=trace_col_ext, zorder=1, linewidth=trace_lw)
ax4.plot(t_vec[del_start_ix-1:del_end_ix], dat_ext[del_start_ix-1:del_end_ix], color=trace_col_ext, zorder=1, linewidth=trace_lw)
ax4.plot(t_vec[del_end_ix-1:], dat_ext[del_end_ix-1:], color=trace_col_ext, zorder=1, linewidth=trace_lw)

# flexor

ax4.plot(t_vec[:del_start_ix], dat_flx[:del_start_ix]+trace_offset, color=trace_col_flx, zorder=1, linewidth=trace_lw)
ax4.plot(t_vec[del_start_ix-1:del_end_ix], dat_flx[del_start_ix-1:del_end_ix]+trace_offset, color=trace_col_flx, zorder=1, linewidth=trace_lw)
ax4.plot(t_vec[del_end_ix-1:], dat_flx[del_end_ix-1:]+trace_offset, color=trace_col_flx, zorder=1, linewidth=trace_lw)

#ax4.hlines(1.4, t_vec[del_end_ix+trim_len], t_vec[-trim_len-1], color="k")
ax4.set_ylim([-0.7,1.4])
ax4.plot([t_vec[0], t_vec[100]], [-0.7, -0.7], color="k", linewidth=2)
label_xoffset = -1.2
ext_lab_yoffset = 0.25
flx_lab_yoffset = -0.5
del_label_offset = -75
if plot_extra_labels:    
    # state space titles 
    event_name = "Deletion"
    #event_name = "attenuation"
    ax1.set_title(f"Pre-{event_name}", fontsize=fs)
    ax2.set_title(f"{event_name}", fontsize=fs)
    ax3.set_title(f"Post-{event_name}", fontsize=fs)

    # add extensor and flexor labels    
    ax4.text(label_xoffset, ext_lab_yoffset, "Extensor", rotation=90, color=trace_col_ext, fontsize=fs)
    ax4.text(label_xoffset, flx_lab_yoffset, "Flexor", rotation=90, color=trace_col_flx, fontsize=fs)

    # state space extension/flexion labels
    ax1.text(2, -7.5, "Extension", color=c1, fontsize=fs)
    ax1.text(8,  10, "Flexion", color=c2, fontsize=fs)
    trim_len = 0

    # add scalebar label
    ax4.text(t_vec[0], -0.9, "1s", color="k", fontsize=fs)
    # deletion bar and label over EMG traces 
    ax4.hlines(1.4, t_vec[del_start_ix+trim_len], t_vec[del_end_ix-trim_len], color="k")    
    ax4.text(t_vec[del_start_ix+del_label_offset], 1.5, f"{event_name}")
else:
    axs = [ax1, ax2, ax3]
    for ax in axs:
        ax.set_title("a", fontsize=fs, color="white")
    ax4.text(label_xoffset, ext_lab_yoffset, "Extensor", rotation=90, color="white")
    ax4.text(label_xoffset, flx_lab_yoffset, "Flexor", rotation=90, color="white")
    ax4.text(t_vec[del_start_ix+del_label_offset], 1.5, "Deletion", color="white")
    ax4.text(t_vec[0], -0.9, "1s", color="white", fontsize=fs)
# shade deletion area
ax4.axvspan(xmin=t_vec[del_start_ix-1], xmax=t_vec[del_end_ix], alpha=0.2, color="gray")

#ax4.set_ylabel("extensor", fontsize=fs)
#ax4.set_xlabel("Time (s)")
ax4.get_xaxis().set_visible(False)    
ax4.spines["bottom"].set_visible(False)
ax4.spines["left"].set_visible(False)

axs = [ ax1, ax2, ax3, ax4]

for ax in axs:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)    
ss_axs = [ ax1, ax2, ax3]
for ax in ss_axs:
    
    ax.set_xlim(-10, 16)
    ax.set_ylim(-10, 16)
    ax.set_aspect("equal")
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    # scale bar and labels
    ax.plot([corner, corner], [corner, corner+length], color="k", linewidth=2)
    ax.plot([corner, corner+length], [corner, corner], color="k", linewidth=2)
    ax.text(corner+xlab_offset, corner+lab_offset, s="PC1",)
    ax.text(corner+lab_offset, corner+ylab_offset, s="PC2", rotation=90)

ax4.set_yticks([])
fig.tight_layout()

plt.show()