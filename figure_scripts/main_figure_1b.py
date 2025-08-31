# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.cm as colormap
from mpl_toolkits.mplot3d import Axes3D
from utils.utils import read_state_space_data

sd_path = "../data/SourceData.xlsx"

C_ID = 1
cname = f"c{C_ID}"

sdp_2ff = read_state_space_data(sd_path, sheet_name=f"Fig1B_{cname}")
# %% [ SOURCE DATA PLOT - MAIN FIGURE 1B ]

fs = 10
edge_buffer = 2 
cycle_range = None    
cm = colormap.bone_r
alpha = 0.7
border_lw = 1
border_c = "k" # color
border_a = 1.0 # alpha

if cname == "c2":    
    edge_buffer = 0.5
    xlims = [-0.8, 0.8]
    ylims = [-0.2, 1.0]
    zlims = [-5, 5] 
    azim = -25 
    elev = 55
    ydim = 1
    xdim = 0 
elif cname == "c1":    
    edge_len = 0.75
    ylims = [-edge_len, edge_len-0.2] 
    xlims = [-edge_len, edge_len-0.1]     
    edge_buffer = 0.5    
    zlims = [-7, 5]      
    azim = 50
    elev = 45
    ydim = 0
    xdim = 0

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
    c_val = sdp2f['c_val']
    
    c = cm(c_val)[:3]
    # constants
    lw = 0.5    
    
    ax.plot(dat[t_ix:-t_ix, 0], dat[t_ix:-t_ix, 1], dat[t_ix:-t_ix, 2], '-', markersize=2, zorder=3, color=c, alpha=alpha, linewidth=lw)

    # whether to plot shadows        
    proj_alpha = 0.01
    proj_c = c
    if xlims is not None:
        ax.plot(dat[t_ix:-t_ix, 1], dat[t_ix:-t_ix, 2], '-', zdir="x", zs=xlims[0], color=proj_c, zorder=1, alpha=proj_alpha, linewidth=lw)
    if zlims is not None:
        ax.plot(dat[t_ix:-t_ix, 0], dat[t_ix:-t_ix, 1], '-', zdir="z", zs=zlims[0], color=proj_c, zorder=1, alpha=proj_alpha, linewidth=lw)
    if ylims is not None:                    
        ax.plot(dat[t_ix:-t_ix, 0], dat[t_ix:-t_ix, 2], '-', zdir="y", zs=ylims[ydim], color=proj_c, zorder=1, alpha=proj_alpha, linewidth=lw)

# TODO: add keyword argument so function isn't dependent on variable outside function namespace
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

ax.plot([xlims[0], xlims[0]],[ylims[0], ylims[0]], [zlims[0], zlims[1]], color=border_c, linewidth=border_lw, zorder=1)
ax.plot([xlims[0], xlims[0]],[ylims[0], ylims[1]], [zlims[0], zlims[0]], color=border_c, linewidth=border_lw, zorder=1)   

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
    ax_lw = 1 # 3
    axis.line.set_linewidth(ax_lw)
    axis.set_tick_params(width=ax_lw)    
lab_shift = -10 # 6
ax.zaxis.labelpad = lab_shift
ax.xaxis.labelpad = lab_shift + 2
ax.yaxis.labelpad = lab_shift + 1
fig.tight_layout()

plt.show()