import os
import pdb
import json
import sys
import time
from PIL import Image
import numpy as np
import pydicom
import pandas as pd
import cv2

import matplotlib.pyplot as plt


from sklearn.metrics import log_loss, roc_auc_score
# from skimage.metrics import structural_similarity as ssim

raw_dicoms_path = '/sddata/projects/Challenges/XAI/utils/dicom_images'
predictions_output = '/sddata/projects/Challenges/XAI/utils/saliency_maps'
png_output = '/sddata/projects/Challenges/XAI/utils/pngs'
reference = '/sddata/projects/Challenges/XAI/utils/pmaps'
reference_png = '/sddata/projects/Challenges/XAI/utils/pmaps_pngs'
utils = '/sddata/projects/Challenges/XAI/utils'


def read_dicoms():
    dicom_files = [f for f in os.listdir(raw_dicoms_path) if f.endswith('.dcm')]
    input_np_arrays = {f:pydicom.dcmread(os.path.join(raw_dicoms_path, f)).pixel_array for f in dicom_files}
    # neg_cases = ['1.2.826.0.1.3680043.10.474.232451.45328.dcm', '1.2.826.0.1.3680043.10.474.232451.50262.dcm', '1.2.826.0.1.3680043.10.474.514382.801109.dcm']
    # for neg_case in neg_cases:
    #     neg_case_npy = pydicom.dcmread(os.path.join(raw_dicoms_path, neg_case)).pixel_array
    #     neg_case_pmap_npy = zeros_array = np.zeros(neg_case_npy.shape)
    #     np.save(os.path.join(reference, neg_case.replace(".dcm", ".npy")), neg_case_pmap_npy)
    return input_np_arrays


input_np_arrays = read_dicoms()
input_np_arrays['1.2.276.0.7230010.3.1.4.8323329.23517.1517874448.532544.dcm'].shape # (1024, 1024)
# Plotting the data
# plt.imshow(input_np_arrays['1.2.276.0.7230010.3.1.4.8323329.23517.1517874448.532544.dcm'], cmap='gray')
# Saving the plot as a PNG file
# plt.savefig(os.path.join(raw_dicoms_path, '1.2.276.0.7230010.3.1.4.8323329.23517.1517874448.532544.png'))
# plt.close()  # Close the plot to free up memory


def read_saliency_map_predictions():
    map_files = [f for f in os.listdir(predictions_output) if f.endswith('.npy')]
    output_pred_arrays = {f:np.load(os.path.join(predictions_output, f)) for f in map_files}
    return output_pred_arrays

output_pred_arrays = read_saliency_map_predictions()
output_pred_arrays['1.2.276.0.7230010.3.1.4.8323329.23517.1517874448.532544.npy'].shape # (299, 299)
len(output_pred_arrays)


def read_ref_pmaps():
    ref_files = [f for f in os.listdir(reference) if f.endswith('.npy')]
    ref_arrays = {f:np.load(os.path.join(reference, f)) for f in ref_files}
    return ref_arrays

ref_arrays = read_ref_pmaps()
ref_arrays['1.2.276.0.7230010.3.1.4.8323329.23517.1517874448.532544.npy'].shape # (1024, 1024)
len(ref_arrays)



# --------------
def upsample_saliency_map(saliency_map, gt_mask, interpolation=cv2.INTER_CUBIC):
    target_size = gt_mask.shape[:2][::-1]
    if saliency_map.ndim == 3 and saliency_map.shape[2] == 3:
        saliency_map = saliency_map.mean(axis=2)
    # Upsample the saliency map
    upsampled_saliency_map = cv2.resize(
        saliency_map, target_size, interpolation=interpolation
    )
    return upsampled_saliency_map



def upsample_saliency_maps():
    output_pred_arrays_l = [output_pred_arrays[k] for k in output_pred_arrays.keys()]
    ref_arrays_l = [ref_arrays[k] for k in ref_arrays.keys()]
    # pdb.set_trace()
    usmaps = {}
    for pred, mask, key_np in zip(output_pred_arrays_l,ref_arrays_l, output_pred_arrays.keys()):
        usmaps[key_np] = upsample_saliency_map(pred, mask, interpolation=cv2.INTER_CUBIC)
    return usmaps


usmaps = upsample_saliency_maps()
usmaps['1.2.276.0.7230010.3.1.4.8323329.23517.1517874448.532544.npy'].shape # (1024, 1024)
len(usmaps)


def convert_to_pngs(arr, directory):
    predictions_8_bit = {prediction_key:(arr[prediction_key]*255).astype(np.uint8) for prediction_key in arr.keys()}
    for f in predictions_8_bit.keys():
        # im = Image.fromarray((predictions_8_bit[f] * 255 + 0.5).astype(np.uint8)) 
        # im = Image.fromarray(np.round(predictions_8_bit[f] * 255)) # New
        im = Image.fromarray(predictions_8_bit[f]) # New Upasana, maybe?
        print(im.size) # (1024, 1024)
        im.save(os.path.join(directory, f.replace('.npy','.png')))
    return predictions_8_bit


us_output_pred_arrays_npys = convert_to_pngs(usmaps, utils)
ref_arrays_8_bit = convert_to_pngs(ref_arrays, reference_png)


def convert_from_pngs(us_output_pred_arrays_npys):
    loaded_images_0_1 = {}
    for f in us_output_pred_arrays_npys.keys():
        loaded_image_255 = np.array(Image.open(os.path.join(utils, f.replace('.npy','.png'))))
        # pdb.set_trace()
        print(loaded_image_255.shape)
        loaded_image_0_1 = loaded_image_255.astype(np.float32) / 255.0  # Convert back to float and scale to 0-1
        loaded_images_0_1[f] = loaded_image_0_1
    return loaded_images_0_1


us_loaded_images_0_1 = convert_from_pngs(us_output_pred_arrays_npys)
us_loaded_images_0_1['1.2.276.0.7230010.3.1.4.8323329.23517.1517874448.532544.npy']

a = us_loaded_images_0_1['1.2.276.0.7230010.3.1.4.8323329.23517.1517874448.532544.npy']
b = usmaps['1.2.276.0.7230010.3.1.4.8323329.23517.1517874448.532544.npy']
a-b


# Stats and Metrics
from sklearn.metrics import log_loss, roc_auc_score

# Weighted Log Loss
wll_list = []
ref_img_list = [f for f in os.listdir(reference) if f.endswith('.npy')]
pred_img_list = [f for f in os.listdir(reference) if f.endswith('.npy')]
# pred_img_list = [f for f in os.listdir(utils) if f.endswith('.png')]
ref_img_list.sort()
pred_img_list.sort()
for i, (ref_img, pred_img) in enumerate(zip(ref_img_list, pred_img_list)):
    print(f"On image {i+1} | {ref_img}")
    ref_np = np.load(os.path.join(reference, ref_img))
    ## Raw upscale check
    pred_np = usmaps[pred_img]
    ## CONVER REF TO PNG
    im = Image.fromarray((pred_np * 255).astype(np.uint8)) 
    im.save(os.path.join(png_output, pred_img.replace('.npy','.png')))
    loaded_image_255 = np.array(Image.open(os.path.join(png_output,  pred_img.replace('.npy','.png'))))
    loaded_image_0_1 = loaded_image_255.astype(np.float32) / 255.0  # Convert back to float and scale to 0-1
    pred_np = loaded_image_0_1
    # print(type(loaded_image_0_1))
    # print(loaded_image_0_1.shape)
    # pdb.set_trace()
    # compare_arrays(pred_np, loaded_image_0_1)
    ## CONVER REF TO PNG
    ## Raw upscale check
    ## SCORING PROGRAM
    # pred_png = Image.open(os.path.join(utils, pred_img))
    # pred_np = np.array(pred_png).astype(np.float32) / 255.0
    ## SCORING PROGRAM
    # Ensure the same shape for both reference and prediction arrays
    assert ref_np.shape == pred_np.shape, f"Shape mismatch: {ref_np.shape} vs {pred_np.shape}"
    ref_binarized = np.where(ref_np > 0, 1, 0)
    ref_pmap_to_weights = np.where(ref_np == 0, 1,
                          np.where((ref_np == 1/3), 15,
                          np.where((ref_np == 2/3), 30,
                          np.where((ref_np == 1), 45, 1))))
    # pdb.set_trace()
    wll = log_loss(ref_binarized.flatten(), pred_np.flatten(), sample_weight=ref_pmap_to_weights.flatten())
    wll_list.append(wll)










def compare_arrays(array1, array2):
    """
    Compare two NumPy arrays for similarity.
    Args:
        array1 (np.ndarray): The first array.
        array2 (np.ndarray): The second array.
    Returns:
        dict: A dictionary containing the results of the comparison.
              Keys include 'identical', 'mse', and 'ssim'.
    """
    if array1.shape != array2.shape:
        raise ValueError("Arrays must have the same shape.")
    # Check if arrays are identical
    identical = np.array_equal(array1, array2)
    # Compute Mean Squared Error (MSE)
    mse_value = np.mean((array1 - array2) ** 2)
    # Compute Structural Similarity Index (SSIM)
    ssim_value = ssim(array1, array2, data_range=array2.max() - array2.min())
    return {
        'identical': identical,
        'mse': mse_value,
        'ssim': ssim_value
    }








import numpy as np
import imageio

def convert_numpy_to_png_and_back(filepath):
    # Load the numpy array
    array = np.load(filepath)
    
    # Ensure the array is in the range 0-1
    assert array.min() >= 0 and array.max() <= 1, "Array values should be between 0 and 1."
    
    # Convert array to an image (PNG)
    image_path = filepath.replace('.npy', '.png')
    imageio.imwrite(image_path, (array * 255).astype(np.uint8))  # Scale to 0-255 and convert to uint8
    
    # Load the image back as a numpy array
    loaded_image = imageio.imread(image_path).astype(np.float32) / 255.0  # Convert back to float and scale to 0-1
    
    # Check for differences
    difference = np.abs(array - loaded_image)
    print(f"Maximum difference after conversion: {difference.max()}")
    print(f"Are all values the same: {np.allclose(array, loaded_image)}")

    return loaded_image

# Example usage
file_path = "/sddata/data/rsna-pneumonia-detection-challenge/ben_testing_10_images/saliency_maps/1.2.276.0.7230010.3.1.4.8323329.2509.1517874296.965359.npy"
converted_array = convert_numpy_to_png_and_back(file_path)




def convert_numpy_to_png_and_back(filepath):
    # Load the numpy array
    array = np.load(filepath)
    # Ensure the array is in the range 0-1
    assert array.min() >= 0 and array.max() <= 1, "Array values should be between 0 and 1."
    # Convert array to an image (PNG)
    image_path = filepath.replace('.npy', '.png')
    im = Image.fromarray((array * 255).astype(np.uint8))  # Scale to 0-255 and convert to uint8
    im.save(image_path)
    # Load the image back as a numpy array
    loaded_image = np.array(Image.open(image_path)).astype(np.float32) / 255.0  # Convert back to float and scale to 0-1
    # Check for differences
    difference = np.abs(array - loaded_image)
    print(f"Maximum difference after conversion: {difference.max()}")
    print(f"Are all values the same: {np.allclose(array, loaded_image)}")
    return loaded_image
# Example usage
file_path = "/sddata/data/rsna-pneumonia-detection-challenge/ben_testing_10_images/saliency_maps/1.2.276.0.7230010.3.1.4.8323329.2509.1517874296.965359.npy"
converted_array = convert_numpy_to_png_and_back(file_path)