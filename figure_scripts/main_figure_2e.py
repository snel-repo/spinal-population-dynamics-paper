# %%
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from utils.utils import read_main_fig2e_data

sd_path = "../data/SourceData.xlsx"

C_ID = 2 
cname = f"c{C_ID}"

sdp_2ff = read_main_fig2e_data(sd_path, sheet_name=f"Fig2E_{cname}")
# %% [ SOURCE DATA PLOT - MAIN FIGURE 2E ]

# constants
edge_buffer = 2 
fs = 10
lw = 0.5    
proj_alpha = 0.01
border_lw = 1
border_c = "k" # color
border_a = 1.0 # alpha

if cname == "c2":
    xlims = [-12.0, 10.0]
    ylims = [-4.0, 14]
    zlims = [-5, 5] 
    azim = -25
    elev = 55
    ydim = 1
    xdim = 0                
elif cname == "c1":
    xlims = [-8.0, 6.0]
    ylims = [-8.5, 5.5]
    zlims = [-7, 5]      
    azim = 50
    elev = 45
    ydim = 0
    xdim = 0

cycle_range = None
    
xlims = [xlims[0]-edge_buffer, xlims[1]+edge_buffer]
ylims = [ylims[0]-edge_buffer, ylims[1]+edge_buffer]


fig = plt.figure(figsize=(3,3), dpi=300)
ax = fig.add_subplot(111, projection="3d")

for sdp2f in sdp_2ff:
    try:
        dat = sdp2f['data']
    except:
        continue
    t_ix = sdp2f['edge_ix']
    switch_ix = sdp2f['switch_ix']

    ax.plot(dat[switch_ix:-t_ix, 0], dat[switch_ix:-t_ix, 1], dat[switch_ix:-t_ix, 2], zorder=2, color="tomato", alpha=0.5, linewidth=lw)
    ax.plot(dat[t_ix:switch_ix, 0], dat[t_ix:switch_ix, 1], dat[t_ix:switch_ix, 2], zorder=3, color="dodgerblue", alpha=0.5, linewidth=lw)
    

    # whether to plot shadows            
    if xlims is not None:
        ax.plot(dat[switch_ix:-t_ix, 1], dat[switch_ix:-t_ix, 2], '-', zdir="x", zs=xlims[xdim], color="tomato", zorder=1, alpha=proj_alpha, linewidth=lw)
        ax.plot(dat[t_ix:switch_ix, 1], dat[t_ix:switch_ix, 2], '-', zdir="x", zs=xlims[xdim], color="dodgerblue", zorder=1, alpha=proj_alpha, linewidth=lw)                
    if zlims is not None:
        ax.plot(dat[switch_ix:-t_ix, 0], dat[switch_ix:-t_ix, 1], '-', zdir="z", zs=zlims[0], color="tomato", zorder=1, alpha=proj_alpha, linewidth=lw)
        ax.plot(dat[t_ix:switch_ix, 0], dat[t_ix:switch_ix, 1], '-', zdir="z", zs=zlims[0], color="dodgerblue", zorder=1, alpha=proj_alpha, linewidth=lw)                                
    if ylims is not None:
        ax.plot(dat[switch_ix:-t_ix, 0], dat[switch_ix:-t_ix, 2], '-', zdir="y", zs=ylims[ydim], color="tomato", zorder=1, alpha=proj_alpha, linewidth=lw)
        ax.plot(dat[t_ix:switch_ix, 0], dat[t_ix:switch_ix, 2], '-', zdir="y", zs=ylims[ydim], color="dodgerblue", zorder=1, alpha=proj_alpha, linewidth=lw)                                                            

if cname == "c2":
    ax.zaxis._axinfo['juggled'] = (1,2,0)

ax.xaxis.set_tick_params(pad=10)
ax.yaxis.set_tick_params(pad=10)
ax.set_xlabel("PC1", fontsize=fs)
ax.set_ylabel("PC2", fontsize=fs)
ax.set_zlabel("PC3", fontsize=fs)

if xlims is not None:
    ax.set_xlim(xlims)
if ylims is not None:
    ax.set_ylim(ylims)
if zlims is not None:    
    ax.set_zlim(zlims)

scale = 1.021
def lims(mplotlims, scale=1.021):
    offset = (mplotlims[1] - mplotlims[0])*scale
    return mplotlims[1] - offset, mplotlims[0] + offset

xlims = lims(ax.get_xlim())
ylims = lims(ax.get_ylim())
zlims = lims(ax.get_zlim())    

ax.grid(False)
ax.xaxis.pane.set_edgecolor('black')
ax.yaxis.pane.set_edgecolor('black')
ax.zaxis.pane.set_edgecolor('black')

ax.zaxis.pane.set_linewidth(border_lw)
ax.xaxis.pane.set_linewidth(border_lw)
ax.yaxis.pane.set_linewidth(border_lw)

ax.zaxis.pane.set_edgecolor(border_c)
ax.xaxis.pane.set_edgecolor(border_c)
ax.yaxis.pane.set_edgecolor(border_c)

ax.zaxis.pane.set_alpha(border_a)
ax.xaxis.pane.set_alpha(border_a)
ax.yaxis.pane.set_alpha(border_a)

ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])
ax.view_init(elev, azim)

for axis in [ax.w_xaxis, ax.w_yaxis, ax.w_zaxis]:
    ax_lw = 1
    axis.line.set_linewidth(ax_lw)
    axis.set_tick_params(width=ax_lw)    
lab_shift = -10
ax.zaxis.labelpad = lab_shift
ax.xaxis.labelpad = lab_shift + 2
ax.yaxis.labelpad = lab_shift + 1
fig.tight_layout()

plt.show()