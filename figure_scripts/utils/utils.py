import pandas as pd
import numpy as np
from matplotlib.path import Path

def read_state_space_data(path, sheet_name="Data",
                           start_row=0, start_col=0,
                           col_gap=1, block_width=3):

    df_all = pd.read_excel(path, sheet_name=sheet_name, header=None)
    records = []
    col0 = start_col

    while col0 < df_all.shape[1]:
        # Stop if cycle header is missing
        cycle_header = df_all.iat[start_row, col0]
        if pd.isna(cycle_header):
            break

        r = start_row + 1
        
        # --- edge_ix ---
        edge_ix = df_all.iat[r, col0+1]
        r += 1
        # --- c_val ---
        c_val = float(df_all.iat[r, col0+1])
        
        r += 2
        # --- skip "data" label row ---
        r += 1
        
        # --- data ---
        data_header = df_all.iloc[r, col0:col0+3].tolist()        
        # --- skip header labels row ---
        r += 1
        arr = []
        while r < df_all.shape[0] and not pd.isna(df_all.iat[r, col0]):
            arr.append(df_all.iloc[r, col0:col0+3].values)
            r += 1
        arr = np.asarray(arr, dtype=float)

        # --- build tx entries back ---
        record = {
            "data": arr,
            "edge_ix" : int(edge_ix) if pd.notna(edge_ix) else None,
            "c_val": c_val
        }

        records.append(record)        

        col0 += block_width + col_gap

    return records

def read_main_fig2e_data(path, sheet_name="Data",
                           start_row=0, start_col=0,
                           col_gap=1, block_width=3):
    
    df_all = pd.read_excel(path, sheet_name=sheet_name, header=None)
    records = []
    col0 = start_col

    while col0 < df_all.shape[1]:
        # Stop if cycle header is missing
        cycle_header = df_all.iat[start_row, col0]
        if pd.isna(cycle_header):
            break

        r = start_row + 1
        
        # --- edge_ix ---
        edge_ix = df_all.iat[r, col0+1]
        r += 1

        # --- switch_ix ---
        switch_ix = df_all.iat[r, col0+1]        
        r += 2
        # --- skip "data" label row ---
        r += 1
        
        # --- data ---
        data_header = df_all.iloc[r, col0:col0+3].tolist()        
        # --- skip header labels row ---
        r += 1
        arr = []
        while r < df_all.shape[0] and not pd.isna(df_all.iat[r, col0]):
            arr.append(df_all.iloc[r, col0:col0+3].values)
            r += 1
        arr = np.asarray(arr, dtype=float)

        # --- build tx entries back ---
        record = {
            "data": arr,
            "edge_ix" : int(edge_ix) if pd.notna(edge_ix) else None,
            "switch_ix" : int(switch_ix) if pd.notna(switch_ix) else None,
        }

        records.append(record)        

        col0 += block_width + col_gap

    return records

def read_main_fig2f_data(path, sheet_name="Data",
                           start_row=0, start_col=0,
                           col_gap=3, block_width=5):

    df_all = pd.read_excel(path, sheet_name=sheet_name, header=None)
    records = []
    col0 = start_col

    while col0 < df_all.shape[1]:
        # Stop if cycle header is missing
        cycle_header = df_all.iat[start_row, col0]
        if pd.isna(cycle_header):
            break

        r = start_row + 1

        # --- tx table ---
        tx_header = df_all.iloc[r, col0:col0+5].tolist()
        if all(pd.isna(x) for x in tx_header):
            break
        r += 1
        tx_rows = []
        while r < df_all.shape[0] and not pd.isna(df_all.iat[r, col0]):
            row_vals = df_all.iloc[r, col0:col0+5].tolist()
            tx_rows.append(row_vals)
            r += 1
        df_tx = pd.DataFrame(tx_rows, columns=["tx_num", "tx_ix", "c1", "c2", "c3"])

        r += 1       
        # --- edge_ix ---
        edge_ix = df_all.iat[r, col0+1]
        r += 1

        # --- switch_ix ---
        switch_ix = df_all.iat[r, col0+1]
        r += 1

        # --- hold_start_ix ---
        hold_start_ix = df_all.iat[r, col0+1]
        r += 1

        # --- hold_stop_ix ---
        hold_stop_ix = df_all.iat[r, col0+1]
        r += 2

        # --- skip "data" label row ---
        r += 1
        
        # --- data ---
        data_header = df_all.iloc[r, col0:col0+3].tolist()        
        r += 1
        arr = []
        while r < df_all.shape[0] and not pd.isna(df_all.iat[r, col0]):
            arr.append(df_all.iloc[r, col0:col0+3].values)
            r += 1
        arr = np.asarray(arr, dtype=float)

        # --- build tx entries back ---
        record = {
            "data": arr,
            "edge_ix" : int(edge_ix) if pd.notna(edge_ix) else None,
            "switch_ix" : int(switch_ix) if pd.notna(switch_ix) else None,
            "hold_start_ix": int(hold_start_ix) if pd.notna(hold_start_ix) else None,
            "hold_stop_ix": int(hold_stop_ix) if pd.notna(hold_stop_ix) else None,
        }
        for _, row in df_tx.iterrows():
            tx_num = int(row["tx_num"])
            record[f"tx{tx_num}_ix"] = {
                "tx_ix": int(row["tx_ix"]),
                "color": (
                    float(row["c1"]),
                    float(row["c2"]),
                    float(row["c3"]),
                    1.0,  # restore alpha=1.0 convention
                ),
            }        
        records.append(record)        
        
        
        # move to next block
        col0 += block_width + col_gap
        
    # get planes        
    r = 1 # restart row counter            
    while r < df_all.shape[0]:
        
        def _traverse_col(r):
            s_r = r+1             
            while not pd.isna(df_all.iat[r, start_col]):                
                r += 1
            e_r = r
            plane_len = e_r - s_r

            return s_r, e_r
        if df_all.iat[r, start_col] == "xx":                        
            s_r, e_r = _traverse_col(r)
            plane_len = e_r - s_r
            r = e_r
            
            xx = df_all.iloc[s_r:e_r, start_col:start_col+plane_len].values.astype(float)
            
            
        elif df_all.iat[r, start_col] == "yy":            
            s_r, e_r = _traverse_col(r)
            plane_len = e_r - s_r
            r = e_r            
            yy = df_all.iloc[s_r:e_r, start_col:start_col+plane_len].values.astype(float)
            
        elif df_all.iat[r, start_col] == "zz":            
            s_r, e_r = _traverse_col(r)
            plane_len = e_r - s_r
            r = e_r            
            zz = df_all.iloc[s_r:e_r, start_col:start_col+plane_len].values.astype(float)
            
        elif df_all.iat[r, start_col] == "plane_order":            
            r += 1
            plane_order = df_all.iloc[r:r+4, start_col]
            
            break
        r += 1
    
    records.append({'plane' : (xx, yy, zz),
                    'plane_order': plane_order
                    })



    return records

def read_main_fig4b_data(path, sheet_name="Data",
                           start_row=0, start_col=0,
                           col_gap=1, block_width=4):

    df_all = pd.read_excel(path, sheet_name=sheet_name, header=None)
    records = []
    col0 = start_col

    while col0 < df_all.shape[1]:
        # Stop if cycle header is missing
        cycle_header = df_all.iat[start_row, col0]
        if pd.isna(cycle_header):
            break

        r = start_row + 1
        
        # --- c_val ---
        c_val = float(df_all.iat[r, col0+1])        
        r += 2
        # --- skip "data" label row ---
        r += 1
        
        # --- data ---
        data_header = df_all.iloc[r, col0:col0+3].tolist()        
        # --- skip header labels row ---
        r += 1
        arr = []
        while r < df_all.shape[0] and not pd.isna(df_all.iat[r, col0]):
            arr.append(df_all.iloc[r, col0+1:col0+4].values)
            r += 1
        arr = np.asarray(arr, dtype=float)

        # --- build tx entries back ---
        record = {
            "data": arr,            
            "c_val": c_val
        }

        records.append(record)        

        col0 += block_width + col_gap
        
    col0 = start_col
    r += 5
    p1 = df_all.iloc[r:r+3,col0+1]
    p2 = df_all.iloc[r:r+3,col0+2]
    p_vec = {'p1': p1.values.tolist(), 'p2': p2.values.tolist()}
    return records, p_vec

def draw_error_band(ax, x, y, err, **kwargs):
    # Calculate normals via centered finite differences (except the first point
    # which uses a forward difference and the last point which uses a backward
    # difference).
    dx = np.concatenate([[x[1] - x[0]], x[2:] - x[:-2], [x[-1] - x[-2]]])
    dy = np.concatenate([[y[1] - y[0]], y[2:] - y[:-2], [y[-1] - y[-2]]])
    l = np.hypot(dx, dy)
    nx = dy / l
    ny = -dx / l

    # end points of errors
    xp = x + nx * err
    yp = y + ny * err
    xn = x - nx * err
    yn = y - ny * err

    vertices = np.block([[xp, xn[::-1]],
                         [yp, yn[::-1]]]).T
    vertices = np.vstack([vertices, vertices[0,:]])    
    codes = np.full(len(vertices), Path.LINETO)
    codes[0] = Path.MOVETO
    codes[len(xp)] = Path.MOVETO
    path = Path(vertices, codes)    
    ax.fill(vertices[:,0], vertices[:,1], **kwargs)
    return path