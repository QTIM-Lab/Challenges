# main.py
#
#   This file represents your code that does the inference (and should be
# substituted with your own code).  The script itself takes four arguments,
# which are passed by your "entrypoint.sh", which in turn receives them from the
# administrative wrapper "ingestion" script:
#
# 1. input_images_dir - The path of the folder with the input DICOM images (one
#        per chest radiograph) that your application should perform inference
#        on.
# 2. output_dir - The path of the folder that your application should write
#       output to.  Your application should write two types of files into this
#       output directory:
#        (a) "image-level-classification.csv" - one comma-separated-value file
#            with the numeric classification of each image (as per the challenge
#            instructions); and
#        (b) PNG files, with one corresponding to each input DICOM file, with
#            the files representing the lung opacity likelihoods at each pixel
#            (as per the challenge instructions).  The PNG files should have
#            the same filenames as the input DICOM files, except with the file
#            extensions changed to ".png".
# 3. submission_dir (also called "ingested_program") - this is the folder where
#        your submission zip file contents (including this "main.py") reside.
#
# Our example below has "main()" calling "generate_pred_matrices()" with the
# input directory, output directory, and model filespec.


import os
import pdb
import json
import sys
import time
from PIL import Image
import numpy as np
import pydicom
import pandas as pd
import torch

debug = False

if torch.cuda.is_available():
    with torch.cuda.device(0):  # Sets device to GPU 0
        print("### Test Tensor ###")
        tensor = torch.tensor([1, 2, 3]).cuda()  # Creates tensor on GPU 0
        print(tensor.device)


# function that are custom to the participants: they have to take inputs: input_dir, output_dir, model
# to generate their pred matrices in the output_dir
def generate_pred_matrices(input_dir, output_dir, model):
    input_filenames = [f for f in os.listdir(input_dir) if f.endswith('.dcm')]
    input_np_arrays = [pydicom.dcmread(os.path.join(input_dir, f)).pixel_array for f in input_filenames]
    if debug == False:
        ### SIMULATE DATA GENERATION
        for i, array in enumerate(input_np_arrays):
            print(f"On image {i+1}: {input_filenames[i]}")
            prediction = np.random.rand(*array.shape)
            # Simulated pred matrices in PNG format
            prediction_8_bit = np.floor(prediction*255+0.5).astype(np.uint8)
            os.makedirs(output_dir, exist_ok=True)
            pil_image = Image.fromarray(prediction_8_bit, mode="L")
            pil_image.save(os.path.join(output_dir, input_filenames[i].replace(".dcm",".png")))
        prediction_scores = [np.random.rand(1)[0] for file in input_filenames]
        classifications = pd.DataFrame({"fileNamePath":input_filenames, "score":prediction_scores}) 
        classifications.to_csv(os.path.join(output_dir,"image-level-classifications.csv"), index=None)
    ### DEBUG DATA GENERATION
    else:
        print("Using data you generated not with this program.")


def main():
    # data that can't be seen except by participant algorithm and is input to their algorithm
    input_dir = os.path.abspath(sys.argv[1]) # /app/input_data/
    # this is the predictions folder
    output_dir = os.path.abspath(sys.argv[2]) # /app/output/
    # this is the ingested program (YOU ARE RESPONSIBLE FOR THIS)
    submission_dir = os.path.abspath(sys.argv[3]) # /app/ingested_program
    
    # change to directory of submission if needed
    os.chdir(os.path.join(submission_dir))

    # access your model or other parts of your submission
    model = os.path.join(submission_dir, 'pneumonia.pt')

    generate_pred_matrices(input_dir, output_dir, model)


if __name__ == '__main__':
    main()