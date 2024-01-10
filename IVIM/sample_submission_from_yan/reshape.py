import zipfile, os, numpy as np
from scipy.optimize import curve_fit

def read_data(file_dir, fname, i):
    
    fname_tmp = file_dir + "{:04}".format(i) + fname
    data = np.load(fname_tmp)
    
    return data  

file_dir = 'sample_submission_from_yan/'
f = np.load(os.path.join(file_dir, 'f.npy'))
f.shape # (200, 200, 10)

Dt = np.load(os.path.join(file_dir, 'Dt.npy'))
Dt.shape # (200, 200, 10)

Ds = np.load(os.path.join(file_dir, 'Ds.npy'))
Ds.shape # (200, 200, 10)

# Split each original array into 10 separate arrays of shape (200, 200, 1)
split_f = np.split(f, 10, axis=2)
split_Dt = np.split(Dt, 10, axis=2)
split_Ds = np.split(Ds, 10, axis=2)

# Merge the corresponding frames from the three arrays into new (200, 200, 3) arrays
for i in range(10):
    merged_array = np.concatenate([split_f[i], split_Dt[i], split_Ds[i]], axis=2)
    # Save each merged array into a separate file
    file_name = f"{str(i+1).rjust(4,'0')}_train_solution.npy"
    np.save(os.path.join(file_dir,file_name), merged_array)
    print(f"Saved {file_name}")

