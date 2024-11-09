import os, numpy as np, pdb


def read_data(indir, fname, i, submission=False):
    if submission:
        fname_tmp = os.path.join(indir, f"{fname}")
    else:
        fname_tmp = os.path.join(indir, "{:04}".format(i) + fname)
    data = np.load(fname_tmp)
    
    return data  

def rRMSE_D(x,y,t):
    
    Nx = x.shape[0]
    Ny = x.shape[1]
    
    t_tmp = np.reshape(t, (Nx*Ny,))
    tumor_indice = np.argwhere(t_tmp == 8)
    non_tumor_indice = np.argwhere(t_tmp != 8)
    non_air_indice = np.argwhere(t_tmp != 1)
    non_tumor_air_indice= np.intersect1d(non_tumor_indice,non_air_indice)
    
    x_tmp = np.reshape(x, (Nx*Ny,))
    x_t = x_tmp[tumor_indice]
    x_nt = x_tmp[non_tumor_air_indice]
    
    y_tmp = np.reshape(y, (Nx*Ny,))
    y_t = y_tmp[tumor_indice]
    y_nt = y_tmp[non_tumor_air_indice]
    
    # tumor region
    tmp1 = np.sqrt(np.sum(np.square(y_t)))
    tmp2 = np.sqrt(np.sum(np.square(x_t-y_t)))
    z_t = tmp2 / tmp1
    
    # non-tumor region
    tmp1 = np.sqrt(np.sum(np.square(y_nt)))
    tmp2 = np.sqrt(np.sum(np.square(x_nt-y_nt)))
    z_nt = tmp2 / tmp1
    
    return z_t, z_nt

def rRMSE_f(x,y,t):
    
    Nx = x.shape[0]
    Ny = x.shape[1]
    
    t_tmp = np.reshape(t, (Nx*Ny,))
    tumor_indice = np.argwhere(t_tmp == 8)
    non_tumor_indice = np.argwhere(t_tmp != 8)
    non_air_indice = np.argwhere(t_tmp != 1)
    non_tumor_air_indice= np.intersect1d(non_tumor_indice,non_air_indice)
    
    x_tmp = np.reshape(x, (Nx*Ny,))
    x_t = x_tmp[tumor_indice]
    x_nt = x_tmp[non_tumor_air_indice]
    
    y_tmp = np.reshape(y, (Nx*Ny,))
    y_t = y_tmp[tumor_indice]
    y_nt = y_tmp[non_tumor_air_indice]
    
    # tumor region
    tmp1 = np.sqrt(tumor_indice.shape[0])
    tmp2 = np.sqrt(np.sum(np.square(x_t-y_t)))
    z_t = tmp2 / tmp1
    
    # non-tumor region
    tmp1 = np.sqrt(non_tumor_air_indice.shape[0])
    tmp2 = np.sqrt(np.sum(np.square(x_nt-y_nt)))
    z_nt = tmp2 / tmp1
    
    return z_t, z_nt

# this fucntion computes the rRMSE for one case
def rRMSE_per_case(x_f,x_dt,x_ds,y_f,y_dt,y_ds,t):
    
    R_f_t, R_f_nt = rRMSE_f(x_f, y_f, t)
    R_Dt_t, R_Dt_nt = rRMSE_D(x_dt, y_dt, t)
    R_Ds_t, R_Ds_nt = rRMSE_D(x_ds, y_ds, t)
    
    z =  (R_f_t + R_Dt_t + R_Ds_t)/3 + (R_f_nt + R_Dt_nt)/2
    
    z_t =  (R_f_t + R_Dt_t + R_Ds_t)/3
    
    return z, z_t




def rRMSE_all_cases(x_f,x_dt,x_ds,y_f,y_dt,y_ds,t):
    
    z = np.empty([x_f.shape[2]])
    z_t = np.empty([x_f.shape[2]])
    
    for i in range(x_f.shape[2]):
        z[i], z_t[i] = rRMSE_per_case(x_f[:,:,i],x_dt[:,:,i],x_ds[:,:,i],y_f[:,:,i],y_dt[:,:,i],y_ds[:,:,i],t[:,:,i]) 
        
    return np.average(z), np.average(z_t)
   
