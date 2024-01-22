#!/usr/bin/env python
import sys, os, time, pdb, numpy as np
from utils import read_data, rRMSE_D, rRMSE_f, rRMSE_per_case, rRMSE_all_cases

input_dir = sys.argv[1]
output_dir = sys.argv[2]

submit_dir = os.path.join(input_dir, 'res')
truth_dir = os.path.join(input_dir, 'ref')

if not os.path.isdir(submit_dir):
    print (f"{submit_dir} doesn't exist")


def main():
    if os.path.isdir(submit_dir) == False or os.path.isdir(truth_dir) == False:
        raise Exception("scoring environment not setup right")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Good to make .html early fue to some 
    # mechanisms that are watching for this to
    # report live updates on the platform

    html_filename = os.path.join(output_dir, 'scores.html')
    html_file = open(html_filename, 'w')

    # Read in Participant Submissions for a little QA
    # And to get stubs for their case file names
    ### ALSO a file called metadata is dropped in input/input/res...filter it out

    cases = os.listdir(os.path.join(truth_dir))
    cases = [file for file in cases if file != 'metadata' and file.find("_IVIMParam") != -1]
    # pdb.set_trace()
    # case_number = [int(casesdata[i][:4]) for i in range(0, len(cases))]
    case_stubs = [cases[i][4:] for i in range(0, len(cases))]    
    if (len(set(case_stubs)) != 1):
        raise Exception(f"""
            File names need to have the same stub. ####_<stub>.npy
            Ex:
                0001_ReconstructionParams.npy
                0002_ReconstructionParams.npy
                ...
            You have these files: {case_stubs}
            """)
    submissions_stub = set(case_stubs)
    submissions_stub = list(submissions_stub)[0]
    fname_ivim_gt ='_IVIMParam.npy'
    fname_tissue ='_TissueType.npy'
    fname_fit = submissions_stub # from above
    num_cases = len(cases)
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
        print(i)
        # load gt data
        x = read_data(truth_dir, fname_ivim_gt, i+1)
        
        # load fitted data
        y = read_data(submit_dir, fname_fit, i+1)
        
        # load tissue type data
        gt_t[:,:,i] = read_data(truth_dir, fname_tissue, i+1)
        
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
    # pdb.set_trace()

    if isinstance(rRMSE_final_1, float) and isinstance(rRMSE_final_tumor_1, float):
        # open file
        output_filename = os.path.join(output_dir, 'scores.txt')
        output_file = open(output_filename, 'w') # Don't do too early or submission passes
        # write output
        output_file.write(f"rRMSE: {rRMSE_final_1}\n")
        output_file.write(f"rRMSE_tumor: {rRMSE_final_tumor_1}\n")
        html_file.write(f"rRMSE: {rRMSE_final_1}\n")
        html_file.write(f"rRMSE_tumor: {rRMSE_final_tumor_1}\n")
    else:
        raise Exception("RMSE calcuations failed")



    output_file.close()
    html_file.close()

if __name__ == "__main__":
    main()