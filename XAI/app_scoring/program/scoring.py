import json
import os
import pdb
import sys
import numpy as np
from sklearn.metrics import log_loss, roc_auc_score
from matplotlib import pyplot as plt


reference_dir = os.path.join(sys.argv[1], 'ref')
prediction_dir = os.path.join(sys.argv[1], 'res')
score_dir = sys.argv[2]
print('Reading prediction')

ref_img_list = [i for i in os.listdir(reference_dir) if i.find(".npy") != -1]
pred_img_list = [i for i in os.listdir(prediction_dir) if i.find(".npy") != -1]

wll_list = []
auc_roc_list = []

for i, (ref_img, pred_img) in enumerate(zip(ref_img_list, pred_img_list)):
    print(f"On image {i+1} | {ref_img}")
    # pdb.set_trace()
    ref_np = np.load(os.path.join(reference_dir, ref_img))
    pred_np = np.load(os.path.join(prediction_dir, pred_img))
    
    # Ensure the same shape for both reference and prediction arrays
    assert ref_np.shape == pred_np.shape, f"Shape mismatch: {ref_np.shape} vs {pred_np.shape}"
    
    ref_np[0][0] = 1.0  # This line seems to force the array to be non-zero
    
    ref_binarized = np.where(ref_np > 0, 1, 0)
    ref_pmap_to_weights = np.where(ref_np == 0, 1,
                                   np.where((ref_np > 0) & (ref_np <= 1/3), 15,
                                            np.where((ref_np > 1/3) & (ref_np <= 2/3), 30,
                                                     np.where((ref_np > 2/3) & (ref_np <= 1), 45, 45))))

    # Assuming 'data' is a 2D array (e.g., an image or a heatmap)
    # plt.figure()
    # plt.imshow(ref_np, cmap='viridis', interpolation='none')
    # plt.colorbar()
    # plt.title('Data from .npy file')
    # plt.savefig(os.path.join(reference_dir, f"{ref_img.split('.npy')[0]}.png"))
    
    # np.unique(ref_np)
    # np.unique(ref_pmap_to_weights)
    # np.unique(pred_np)

    # ref_np.shape
    # ref_pmap_to_weights.shape
    # pred_np.shape

    wll = log_loss(ref_binarized.flatten(), pred_np.flatten(), sample_weight=ref_pmap_to_weights.flatten())
    auc_roc = roc_auc_score(ref_binarized.flatten(), pred_np.flatten())

    wll_list.append(wll)
    auc_roc_list.append(auc_roc)

# Aggregate results
average_wll = np.mean(wll_list)
average_auc_roc = np.mean(auc_roc_list)

# pdb.set_trace()
print(f'Average Weighted Log Loss: {average_wll}')
print(f'Average AUC ROC: {average_auc_roc}')

print('Scores:')
scores = {
    'average_wll': average_wll,
    'average_auc_roc': average_auc_roc
}

with open(os.path.join(score_dir, 'scores.json'), 'w') as score_file:
    score_file.write(json.dumps(scores))
with open(os.path.join(score_dir, 'scores.html'), 'w') as html_file:
    html_file.write(json.dumps(scores))
