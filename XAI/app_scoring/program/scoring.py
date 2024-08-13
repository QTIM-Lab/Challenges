import json
import os
import pdb
import sys
import numpy as np
from sklearn.metrics import log_loss, roc_auc_score
import pandas as pd
from PIL import Image
import cv2

reference_dir = os.path.join(sys.argv[1], 'ref')
prediction_dir = os.path.join(sys.argv[1], 'res')
score_dir = sys.argv[2]
print('Reading prediction')

ref_img_list = [i for i in os.listdir(reference_dir) if i.find(".npy") != -1]
pred_img_list = [i for i in os.listdir(prediction_dir) if i.find(".png") != -1]

ref_img_list.sort()
pred_img_list.sort()

def upsample_saliency_map(saliency_map, gt_mask, interpolation=cv2.INTER_CUBIC):
    target_size = gt_mask.shape[:2][::-1]
    if saliency_map.ndim == 3 and saliency_map.shape[2] == 3:
        saliency_map = saliency_map.mean(axis=2)
    # Upsample the saliency map
    upsampled_saliency_map = cv2.resize(
        saliency_map, target_size, interpolation=interpolation
    )
    return upsampled_saliency_map


# Weighted Log Loss
wll_list = {}

for i, (ref_img, pred_img) in enumerate(zip(ref_img_list, pred_img_list)):
    print(f"On image {i+1} | {pred_img}")
    ref_np = np.load(os.path.join(reference_dir, ref_img))
    ## CONVER REF TO PNG
    loaded_image_255 = np.array(Image.open(os.path.join(prediction_dir,  pred_img)))
    loaded_image_0_1 = loaded_image_255.astype(np.float32) / 255.0  # Convert back to float and scale to 0-1
    pred_np = loaded_image_0_1
    assert ref_np.shape == pred_np.shape, f"Shape mismatch: {ref_np.shape} vs {pred_np.shape}"
    ref_binarized = np.where(ref_np > 0, 1, 0)
    ref_pmap_to_weights = np.where(ref_np == 0, 1,
                          np.where((ref_np == 1/3), 15,
                          np.where((ref_np == 2/3), 30,
                          np.where((ref_np == 1), 45, 1))))
    wll = log_loss(ref_binarized.flatten(), pred_np.flatten(), sample_weight=ref_pmap_to_weights.flatten(), labels=[0,1])
    wll_list[pred_img] = wll


# AUC_ROC
try:
    ref_classifications = pd.read_csv(os.path.join(reference_dir,"image-level-classifications.csv"))
except:
    raise Exception("Can't find reference classifications")

try:
    pred_classifications = pd.read_csv(os.path.join(prediction_dir,"image-level-classifications.csv"))
except:
    raise Exception("Can't find prediction classifications")

try:
    from time import sleep;
    # sleep(60*5)
    join = pd.merge(ref_classifications, pred_classifications, on="fileNamePath")
    join = join.rename(columns = {"score_x":"y_true", "score_y":"y_score"})
    y_true = join['y_true']
    y_score = join['y_score']
except:
    raise Exception("Can't match up prediction file names with reference file names")

try:
    auc_roc = roc_auc_score(y_true, y_score)
except:
    raise Exception("Can't compute auc_ROC for some reason")


# Aggregate results

average_wll = np.mean(list(wll_list.values()))

print(f'Average Weighted Log Loss: {average_wll}')
print(f'AUC ROC: {auc_roc}')

print('Scores:')
scores = {
    'average_wll': average_wll,
    'auc_roc': auc_roc
}

# detailed_scores = {f"{k} | wll -> ":wll_list[k] for k in wll_list.keys()}
detailed_scores = wll_list

with open(os.path.join(score_dir, 'scores.json'), 'w') as score_file:
    score_file.write(json.dumps(scores))
with open(os.path.join(score_dir, 'scores.html'), 'w') as html_file:
    html_file.write(f"Weighted Log Loss by Image:\n")
    html_file.write(json.dumps(detailed_scores, indent = 2))

