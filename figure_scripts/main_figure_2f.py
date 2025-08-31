# %%
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from utils.utils import read_main_fig2f_data
sd_path = "../data/SourceData.xlsx"

C_ID = 1
cname = f"c{C_ID}"

sdp_2ff = read_main_fig2f_data(sd_path, sheet_name=f"Fig2F_{cname}", col_gap=1)
# %% [ SOURCE DATA PLOT - MAIN FIGURE 2F ]
fig = plt.figure(figsize=(5,5), dpi=300) # for figure 2
ax = fig.add_subplot(111, projection="3d")

if cname == "c2":
    azim = -25
    elev = 55               
elif cname == "c1":    
    azim = 50
    elev = 45

for sdp2f in sdp_2ff:
    try:
        dat = sdp2f['data']
    except:
        continue
    t_ix = sdp2f['edge_ix']
    switch_ix = sdp2f['switch_ix']
    # constants
    lw = 0.5
    marker_size = 8
    ax.plot(dat[t_ix:switch_ix, 0], dat[t_ix:switch_ix, 1], dat[t_ix:switch_ix, 2], zorder=3, color="gray", alpha=0.5, linewidth=lw)
    tx_keys = [ key for key in sdp2f.keys() if 'tx' in key ]
    for tx_key in tx_keys:
        tx_pkt = sdp2f[tx_key]
        osc_ix = tx_pkt['tx_ix']
        pt_color = tx_pkt['color']
        ax.scatter([dat[osc_ix, 0]], [dat[osc_ix, 1]], [dat[osc_ix, 2]], zorder=2, color=pt_color, s=marker_size, linewidths=0.5, edgecolors="k", alpha=0.8)
    hstart_ix = sdp2f['hold_start_ix']    
    hstop_ix = sdp2f['hold_stop_ix']
    ax.plot(dat[hstart_ix:hstop_ix, 0], dat[hstart_ix:hstop_ix, 1], dat[hstart_ix:hstop_ix, 2], zorder=8, color="orange", alpha=0.5, linewidth=1)
sdp2f = sdp_2ff[-1]
xx, yy, zz = sdp2f['plane']
plane_order = sdp2f['plane_order']
l1_order, l2_order, l3_order, l4_order = plane_order
ax.plot_surface(xx, yy, zz, alpha=0.2, color="pink", zorder=2) # zorder=4 for woody
ax.plot([xx[0,0], xx[0,-1]], [yy[0,0], yy[0,-1]], [zz[0,0], zz[0,-1]], zorder=l1_order, linewidth=1, color="k") # back border for woody and gran
ax.plot([xx[0,-1], xx[-1,-1]], [yy[0,-1], yy[-1,-1]], [zz[0,-1], zz[-1,-1]], zorder=l2_order, linewidth=1, color="k") # bottom border for woody, 
ax.plot([xx[-1,0], xx[-1,-1]], [yy[-1,0], yy[-1,-1]], [zz[-1,0], zz[-1,-1]], zorder=l3_order, linewidth=1, color="k") # front border for woody, zorder=1 for gran
ax.plot([xx[-1,0], xx[0,0]], [yy[-1,0], yy[0,0]], [zz[-1,0], zz[0,0]], zorder=l4_order, linewidth=1, color="k") # top border for woody and gran    

ax.set_axis_off()
ax.view_init(elev, azim)
fig.tight_layout()

plt.show()