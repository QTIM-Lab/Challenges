import os
import zipfile
import numpy as np
from scipy.optimize import curve_fit

# reconstruct from noise
file_dir='testing/organizer/'
fname_gt ='_IVIMParam.npy'
fname_tissue ='_TissueType.npy'
fname_fit = '_NoisyFitted.npy'
num_cases = 10
Nx = 200
Ny = 200

gt_f = np.empty([Nx,Ny,num_cases])
gt_Dt = np.empty([Nx,Ny,num_cases])
gt_Ds = np.empty([Nx,Ny,num_cases])
gt_t = np.empty([Nx,Ny,num_cases])

# your solution
f = np.empty([Nx,Ny,num_cases])
Dt = np.empty([Nx,Ny,num_cases])
Ds = np.empty([Nx,Ny,num_cases])
rRMSE_case =np.empty([num_cases])
rRMSE_t_case =np.empty([num_cases])



def read_data(file_dir, fname, i):
    
    fname_tmp = file_dir + "{:04}".format(i) + fname
    data = np.load(fname_tmp)
    
    return data  



# this fucntion computes the rRMSE for one microstructual parameter image for each case
# y is the reference solution
# t is the tissue type image
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






# bi-exponential function
def funcBiExp(b, f, Dt, Ds):
    ## Units
    # b: s/mm^2
    # D: mm^2/s
    return (1.-f) * np.exp(-1.*Dt * b) + f * np.exp(-1.*Ds * b)
    

def fit_biExponential_model(arr3D_imgk, arr1D_b):
    arr3D_img = np.abs(np.fft.ifft2(arr3D_imgk, axes=(0,1) ,norm='ortho'))
    arr2D_coordBody = np.argwhere(arr3D_img[:,:,0]>0)
    arr2D_fFitted = np.zeros_like(arr3D_img[:,:,0])
    arr2D_DtFitted = np.zeros_like(arr3D_img[:,:,0])
    arr2D_DsFitted = np.zeros_like(arr3D_img[:,:,0])
    for arr1D_coord in arr2D_coordBody:
        try:
            popt, pcov = curve_fit(funcBiExp, arr1D_b[1:]-arr1D_b[0], arr3D_img[arr1D_coord[0],arr1D_coord[1],1:]/arr3D_img[arr1D_coord[0],arr1D_coord[1],0]
                                , p0=(0.15,1.5e-3,8e-3), bounds=([0, 0, 3.0e-3], [1, 2.9e-3, np.inf]), method='trf')
        except:
            popt = [0, 0, 0]
            print('Coord {} fail to be fitted, set all parameters as 0'.format(arr1D_coord))
        arr2D_fFitted[arr1D_coord[0], arr1D_coord[1]] = popt[0]
        arr2D_DtFitted[arr1D_coord[0], arr1D_coord[1]] = popt[1]
        arr2D_DsFitted[arr1D_coord[0], arr1D_coord[1]] = popt[2]
    return arr2D_fFitted,arr2D_DtFitted,arr2D_DsFitted
    

# Manually read some things
file_dir='reference_data/testing/'
fname_noisyDWIk = '_NoisyDWIk.npy'
fname_gtDWIs = '_gtDWIs.npy'
fname_TissueType = '_TissueType.npy'
fname_IVIMParam = '_IVIMParam.npy'

# Each of these are single cases:
kSpace = read_data(file_dir+'user/', fname_noisyDWIk, 1)
kSpace.shape # (200, 200, 8)

RealImage = read_data(file_dir+'organizer/', fname_gtDWIs, 1)
RealImage.shape # (200, 200, 8)

TissueType = read_data(file_dir+'organizer/', fname_TissueType, 1)
TissueType.shape # (200, 200)
np.unique(TissueType)

IVIMParam = read_data(os.path.join(file_dir,"organizer")+"/", fname_IVIMParam, 1)
IVIMParam.shape # (200, 200, 3)
IVIM_f = IVIMParam[:,:,0]
IVIM_Dt = IVIMParam[:,:,1]
IVIM_Ds = IVIMParam[:,:,2]

b = np.array([0, 5, 50, 100, 200, 500, 800, 1000])

f, Dt, Ds = fit_biExponential_model(kSpace, b) # Took 5 min
f.shape # (200, 200)
Dt.shape # (200, 200)
Ds.shape # (200, 200)

# Specific Case
z, z_t = rRMSE_per_case(IVIM_f\
                       ,IVIM_Dt\
                       ,IVIM_Ds\
                       ,f\
                       ,Dt\
                       ,Ds\
                       ,TissueType)


# You need to do this for all cases to calculate the average of these.
# compute the average rRMSE for all cases

# rRMSE_case => list of (z) values
# rRMSE_t_case => list of (z_t) values

# rRMSE_final_1 = np.average(rRMSE_case)
# rRMSE_final_tumor_1 = np.average(rRMSE_t_case)