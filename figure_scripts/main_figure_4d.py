# %%
import numpy as np
import matplotlib.pyplot as plt
import colorcet as cc
from mpl_toolkits.mplot3d import Axes3D
from utils.utils import read_state_space_data
sd_path = "../data/SourceData.xlsx"

C_ID = 1
cname = f"c{C_ID}"

sdp_2ff = read_state_space_data(sd_path, sheet_name=f"Fig4D_{cname}")
# %% [ SOURCE DATA PLOT - MAIN FIGURE 4D ]

fs = 10
border_lw = 1
border_c = "k" # color
edge_buffer= 0.5
azim = 0
elev = 90

if cname == "c2":
    xlims = [-12.0, 10.0]
    ylims = [-4.0, 14]
    zlims = [-5, 5] 
    ydim = 1
    xdim = 0            
    ss = 1.01
    xlab_shift_fac = 1.15 
    shift_fac = 1.45  

elif cname == "c1":
    xlims = [-8.0, 6.0] 
    ylims = [-8.5, 5.5] 
    zlims = [-7, 5]  
    ydim = 0
    xdim = 0
    # "ss" is the scale factor for the placement of the scale bar. 1 is at the xlim/ylim border, <1 closer toward plot 
    ss = 0.80
    xlab_shift_fac = 1.25 
    shift_fac = 1.2               


xlims = [xlims[0]-edge_buffer, xlims[1]+edge_buffer]
ylims = [ylims[0]-edge_buffer, ylims[1]+edge_buffer]
cycle_range = None    

# constants
cm = cc.m_kbc
alpha = 0.7
sbar_length = 3    
border_lw = 1.5
lw = 0.5        

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
    ax.plot(dat[t_ix:-t_ix, 0], dat[t_ix:-t_ix, 1], dat[t_ix:-t_ix, 2], '-', markersize=2, zorder=3, color=c, alpha=alpha, linewidth=lw)    
    

# --- plot scalebars
ax.plot([xlims[1]*ss, xlims[1]*ss],[ylims[0]*ss, ylims[0]*ss+sbar_length], [0, 0], color=border_c, linewidth=border_lw, zorder=1)
ax.plot([xlims[1]*ss-sbar_length, xlims[1]*ss],[ylims[0]*ss, ylims[0]*ss], [0, 0], color=border_c, linewidth=border_lw, zorder=1)

mean_x = np.mean([xlims[1]*ss, xlims[1]*ss-sbar_length])
max_x = np.max([xlims[1]*ss, xlims[1]*ss-sbar_length])
mean_y = np.mean([ylims[0]*ss, ylims[0]*ss+sbar_length])
min_y = np.min([ylims[0]*ss, ylims[0]*ss+sbar_length])
ax.text(max_x*xlab_shift_fac, mean_y, 0, "PC2", ha="center", va="center", fontsize=fs, color="k", zorder=1)    
ax.text(mean_x,min_y*shift_fac, 0, "PC1", ha="center", va="center", fontsize=fs, color="k", zorder=1)

if xlims is not None:
    ax.set_xlim(xlims)
if ylims is not None:
    ax.set_ylim(ylims)
if zlims is not None:    
    ax.set_zlim(zlims)

scale = 1.021
#ax.invert_yaxis()
def lims(mplotlims, scale=1.021):
    
    offset = (mplotlims[1] - mplotlims[0])*scale
    return mplotlims[1] - offset, mplotlims[0] + offset
xlims = lims(ax.get_xlim())
ylims = lims(ax.get_ylim())
zlims = lims(ax.get_zlim())    

ax.grid(False)
ax.view_init(elev, azim)
ax.set_axis_off()

fig.tight_layout()

plt.show()