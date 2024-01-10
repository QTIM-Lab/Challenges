# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 20:57:52 2023

@author: Xiaoyu Hu
"""

import zipfile
import numpy as np
from scipy.optimize import curve_fit

# this function unzips the target file to the destination path.
# need to use 'import zipfile'
def unzip_data(target_dir, des_dir):
    zipfile.ZipFile(target_dir, 'r').extractall(des_dir)
   

# this function reads an npy file for case i
# need to use 'import  numpy as np'
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


# this fucntion computes the rRMSE for all cases
# y is the reference solution
def rRMSE_all_cases(x_f,x_dt,x_ds,y_f,y_dt,y_ds,t):
    
    z = np.empty([x_f.shape[2]])
    z_t = np.empty([x_f.shape[2]])
    
    for i in range(x_f.shape[2]):
        z[i], z_t[i] = rRMSE_per_case(x_f[:,:,i],x_dt[:,:,i],x_ds[:,:,i],y_f[:,:,i],y_dt[:,:,i],y_ds[:,:,i],t[:,:,i]) 
        
    return np.average(z), np.average(z_t)
   

# this function saves the data to the required format and zip them into one file
# note that the data must be saved in the same folder
def save_zip_data(data_f, data_Dt, data_Ds):
    
    np.save('f.npy', data_f)
    np.save('Dt.npy', data_Dt)
    np.save('Ds.npy', data_Ds)
    
    files_to_zip = ['f.npy', 'Dt.npy', 'Ds.npy'] 
    
    results_name = "solution.zip" 
    
    with zipfile.ZipFile(results_name, "w", zipfile.ZIP_DEFLATED) as zf: 
        for file in files_to_zip: 
            zf.write(file) 
            
            
            
# this function performs a basic reconstruction (inverse FT, then pixel-wise data fitting on magnitude image).
# need to use 'from scipy.optimize import curve_fit'  

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
    
#def main():   
    

#if __name__ == '__main__':
#    main()

file_dir_org='reference_data/testing/organizer/'
file_dir_usr='reference_data/testing/user/'
fname_gt ='_IVIMParam.npy'
fname_tissue ='_TissueType.npy'
fname_fit = '_NoisyDWIk.npy'
# fname_fit = '_IVIMParam.npy' # GT Test
# fname_fit = '_NoisyFitted.npy' # not present
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

for i in range(num_cases):
    
    # load gt data
    x = read_data(file_dir_org, fname_gt, i+1)
    
    # load fitted data
    y = read_data(file_dir_usr, fname_fit, i+1)
    # y = read_data(file_dir_org, fname_fit, i+1) # GT Test
    
    # load tissue type data
    gt_t[:,:,i] = read_data(file_dir_org, fname_tissue, i+1)
    
    # write to the required format 
    gt_f[:,:,i] = x[:,:,0]
    gt_Dt[:,:,i] = x[:,:,1]
    gt_Ds[:,:,i] = x[:,:,2]
    
    # 
    f[:,:,i] = y[:,:,0]
    Dt[:,:,i] = y[:,:,1]
    Ds[:,:,i] = y[:,:,2]
    
    # compute the rRMSE 
    rRMSE_case[i], rRMSE_t_case[i] = rRMSE_per_case(f[:,:,i], Dt[:,:,i], Ds[:,:,i], gt_f[:,:,i], gt_Dt[:,:,i], gt_Ds[:,:,i], gt_t[:,:,i])
   

# compute the average rRMSE for all cases
rRMSE_final_1 = np.average(rRMSE_case)
rRMSE_final_tumor_1 = np.average(rRMSE_t_case)

# save and zip data for submission
output_dir = 'C:/XH/Research/dMRI/output/'
save_zip_data( f, Dt, Ds)


## test for the platform 
## For Ben
## once the participant uploaded their solution sucessfully, you can write a code to compute the final metric.
unzip_data('C:/XH/Research/dMRI/solution.zip', './test')

sol_f = np.load('C:/XH/Research/dMRI/test/f.npy')
sol_Dt = np.load('C:/XH/Research/dMRI/test/Dt.npy')
sol_Ds = np.load('C:/XH/Research/dMRI/test/Ds.npy')

rRMSE_final_2,rRMSE_final_tumor_2 = rRMSE_all_cases(sol_f,sol_Dt,sol_Ds,gt_f, gt_Dt, gt_Ds, gt_t)


## Manually read some things
file_dir='training/'
fname_noisyDWIk = '_NoisyDWIk.npy'
fname_gtDWIs = '_gtDWIs.npy'
fname_TissueType = '_TissueType.npy'
fname_IVIMParam = '_IVIMParam.npy'
kSpace = read_data(file_dir, fname_noisyDWIk, 1)
kSpace.shape # (200, 200, 8)
RealImage = read_data(file_dir, fname_gtDWIs, 1)
RealImage.shape # (200, 200, 8)
TissueType = read_data(file_dir, fname_TissueType, 1)
TissueType.shape # (200, 200)
IVIMParam = read_data(file_dir, fname_IVIMParam, 1)
IVIMParam.shape # (200, 200, 3)
b = np.array([0, 5, 50, 100, 200, 500, 800, 1000])

## test reconstruction script
f, Dt, Ds = fit_biExponential_model(kSpace, b)
## Test rRMSE_per_case
z1, z2 = rRMSE_per_case(f,Dt,Ds,IVIMParam[:,:,0],IVIMParam[:,:,1],IVIMParam[:,:,2],TissueType)
z3, z4 = rRMSE_per_case(IVIMParam[:,:,0],IVIMParam[:,:,1],IVIMParam[:,:,2],\
                        IVIMParam[:,:,0],IVIMParam[:,:,1],IVIMParam[:,:,2],TissueType)
print(z1, z2, z3, z4)