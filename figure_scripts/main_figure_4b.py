# %%
import matplotlib.pyplot as plt
import colorcet as cc
from mpl_toolkits.mplot3d import Axes3D
from utils.utils import read_main_fig4b_data

sd_path = "../data/SourceData.xlsx"

C_ID = 1 # 1 for Cat 1, 2 for Cat 2
cname = f"c{C_ID}"

records, p_vec = read_main_fig4b_data(sd_path, sheet_name=f"Fig4B_{cname}")
# %% [ SOURCE DATA PLOT - MAIN FIGURE 4B ]

fig = plt.figure(figsize=(2.5,2.5), dpi=300)
ax = fig.add_subplot(111, projection="3d")

# flip PC axis using "dirs"
xdir = 1
ydir = 1
zdir = 1

# select which dimensions of trajectory to plot
dim1 = 0
dim2 = 1
dim3 = 2

edge_buffer = 2 # 8 ms for gran       
if cname == "c1":
    box_len = 8
    zscale = 5    
    xlims = [-8.0, 6.0]
    ylims = [-8.5, 5.5]
    zlims = [-7, 5]            
    ydim = 0 
    tick_space = 4
elif cname == "c2":
    box_len = 11
    zscale = 3
    xlims = [-12.0, 10.0]
    ylims = [-4.0, 14]
    zlims = [-5, 5] 
    ydim = 1
    tick_space = 5
    
xlims = [xlims[0]-edge_buffer, xlims[1]+edge_buffer]
ylims = [ylims[0]-edge_buffer, ylims[1]+edge_buffer]

tick_fs = 8
fs = 10
marker_size = 8
lw = 0.5
point_alpha = 0.8    
cm = cc.m_kbc

for i, record in enumerate(records):
    traj = record['data']
    c_val = record['c_val']
    # traj = trajs[mo]
    # c_val = (mags[mo]-MIN_MAG)/(MAX_MAG-MIN_MAG)
    proj_c = cm(c_val)
# plot trajectory
    
    
    # start point
    ax.scatter([traj[0,dim1]*xdir],
                [traj[0,dim2]*ydir],
                [traj[0,dim3]*zdir], 
                marker="o", s=marker_size, 
                color="seagreen", alpha=point_alpha, 
                edgecolors="k", linewidths=0.3, zorder=2
    )
    # end point
    ax.scatter([traj[-1,dim1]*xdir],
               [traj[-1,dim2]*ydir], 
               [traj[-1,dim3]*zdir], 
               marker="o", s=marker_size, 
               color="darkorange", alpha=point_alpha, 
               edgecolors="k", linewidths=0.3, zorder=2
    )
    # trajectory
    ax.plot(traj[:,dim1]*xdir, 
            traj[:,dim2]*ydir,
            traj[:,dim3]*zdir, 
            "-", linewidth=lw, 
            markersize=1, color=proj_c, 
            alpha=0.8, zorder=3
    )
    

p1 = p_vec['p1']
p2 = p_vec['p2']
ax.plot([p1[dim1]*xdir, p2[dim1]*xdir], [p1[dim2]*ydir, p2[dim2]*ydir], [p1[dim3]*zdir, p2[dim3]*zdir], '-o', linewidth=2, markersize=2, color='fuchsia', zorder=4)

if cname == "c2":
    ax.zaxis._axinfo['juggled'] = (1,2,0)
    azim = -25 # -25 # -25 # 75
    elev = 55 # 85    
    
elif cname == "c1":    
    azim = 45 # 45 # 45 # 75
    elev = 50 # 50 # 45

ax.view_init(elev, azim) # gran

ax.set_xlim(xlims)
ax.set_ylim(ylims)
ax.set_zlim(zlims)

ax.set_axis_off()
ax.dist = 6
fig.tight_layout(pad=1)

plt.show()