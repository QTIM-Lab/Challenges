# takes input 
# 1. input_images_dir: location of input images (containing np arrays)
# 2. output_dir: location output predictions (containing np arrays)
# 3. Model in ‘model.pt’ format
# And uses the model.pt and images in the ‘input_images_dir’ to create 
# prediction matrices that are stored as ‘<image_name>.npy’ inside the 

import os
import pdb
import json
import sys
import time
import numpy as np
import pydicom
import pandas as pd

# function that are custom to the participants: they have to take inputs: input_images_dir, output_dir, model
# to generate their pred matrices in the output_dir
def generate_pred_matrices(input_images_dir, output_dir, model):
    input_filenames = [f for f in os.listdir(input_images_dir) if f.endswith('.dcm')]
    input_np_arrays = [pydicom.dcmread(os.path.join(input_images_dir, f)).pixel_array for f in input_filenames]
    # Simulated pred matrices
    predictions = [np.random.rand(*array.shape) for array in input_np_arrays]
    # pdb.set_trace()
    os.makedirs(output_dir, exist_ok=True)
    for pred, fname in zip(predictions, input_filenames):
        np.save(os.path.join(output_dir, fname.replace(".dcm","")), pred)
    # Classification by image
    predictions = [np.random.rand(1)[0] for file in input_filenames]
    classifications = pd.DataFrame({"fileNamePath":input_filenames, "score":predictions}) 
    classifications.to_csv(os.path.join(output_dir,"image-level-classifications.csv"), index=None)

    
# function required by organizers to run as sanity checks to participants' pred matrices
def pred_matrices_sanity_checks(input_images_dir, output_dir):
    input_filenames = [f for f in os.listdir(input_images_dir) if f.endswith('.npy')]
    input_np_arrays = {f: np.load(os.path.join(input_images_dir, f)) for f in input_filenames}
    output_filenames = [f for f in os.listdir(output_dir) if f.endswith('.npy')]
    
    for file in output_filenames:
        pred_matrix = np.load(os.path.join(output_dir, file))
        # Check if the prediction matrix is in .npy format
        if not file.endswith('.npy'):
            print(f"ERROR: {file} is not in .npy format")
            continue
        # Check if the prediction matrix has the same size as the respective input image
        input_file = file
        if input_file in input_np_arrays:
            input_matrix = input_np_arrays[input_file]
            if pred_matrix.shape != input_matrix.shape:
                print(f"ERROR: {file} does not match the size of the respective input image")
        
        # Check if the prediction matrix only has values between 0 and 1 (inclusive)
        if not np.all((pred_matrix >= 0) & (pred_matrix <= 1)):
            print(f"ERROR: {file} contains values outside the range [0, 1]")
        
        print(f"Sanity checks passed: {file}")

def main():
    # Data that can't be seen except by participant algorithm and is input to their algorithm
    input_dir = os.path.abspath(sys.argv[1]) # /app/input_data/
    # When ingestion, this is the predictions folder
    output_dir = os.path.abspath(sys.argv[2]) # /app/output/
    # When ingestion, this is the ingestion program (we are looking at the file in this directory)
    # Available here in case extra utils are needed
    program_dir = os.path.abspath(sys.argv[3]) # /app/program
    # When ingestion, this is the ingested program (YOU ARE RESPONSIBLE FOR THIS)
    submission_dir = os.path.abspath(sys.argv[4]) # /app/ingested_program

    # pdb.set_trace()

    # path to the 'model.pt'
    model = os.path.join(submission_dir, 'pneumonia.pt')

    generate_pred_matrices(input_dir, output_dir, model)
    pred_matrices_sanity_checks(input_dir, output_dir)


if __name__ == '__main__':
    main()