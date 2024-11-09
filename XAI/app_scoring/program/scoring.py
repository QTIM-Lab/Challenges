import json
import os
import pdb
import sys
import numpy as np
from sklearn.metrics import log_loss, roc_auc_score
import pandas as pd
import pdfplumber
from docx import Document
import re
from PIL import Image
import cv2

reference_dir = os.path.join(sys.argv[1], 'ref')
prediction_dir = os.path.join(sys.argv[1], 'res')
score_dir = sys.argv[2]
print('Reading prediction')

ref_img_list = [i for i in os.listdir(reference_dir) if i.find(".npy") != -1]
pred_img_list = [i for i in os.listdir(prediction_dir) if i.find(".png") != -1]
algorithm_file = [i for i in os.listdir(prediction_dir) if i.find(".pdf") != -1 or i.find(".docx") != -1 or i.find(".txt") != -1]

PHASE = 'test'
# PHASE = 'val'

ref_img_list.sort()
pred_img_list.sort()

def count_words_in_pdf(pdf_path):
    word_count = 0
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            # pdb.set_trace()
            if text:
                # Remove non-alphabetical characters and split into words
                words = re.findall(r'\b\w+\b', text)
                word_count += len(words)
    return word_count


def count_words_in_docx(docx_path):
    word_count = 0
    doc = Document(docx_path)
    for paragraph in doc.paragraphs:
        text = paragraph.text
        # Remove non-alphabetical characters and split into words
        words = re.findall(r'\b\w+\b', text)
        # pdb.set_trace()
        word_count += len(words)
    return word_count


def count_words_in_txt(txt_path):
    word_count = 0
    with open(txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Remove non-alphabetical characters and split into words
            words = re.findall(r'\b\w+\b', line)
            # pdb.set_trace()
            word_count += len(words)
    return word_count


def upsample_saliency_map(saliency_map, gt_mask, interpolation=cv2.INTER_CUBIC):
    target_size = gt_mask.shape[:2][::-1]
    if saliency_map.ndim == 3 and saliency_map.shape[2] == 3:
        saliency_map = saliency_map.mean(axis=2)
    # Upsample the saliency map
    upsampled_saliency_map = cv2.resize(
        saliency_map, target_size, interpolation=interpolation
    )
    return upsampled_saliency_map


if PHASE == 'test':
    # Testing
    # file_path = os.path.join(prediction_dir, 'Fake_Algorithm_Description.pdf')
    # file_path = os.path.join(prediction_dir, 'Fake_Algorithm_Description.docx')
    # file_path = os.path.join(prediction_dir, 'Fake_Algorithm_Description.txt')

    if len(algorithm_file) == 0:
        raise Exception(f"You need 1 file with extension 'pdf','docx' or 'txt' that has your algorithm description. Minimum of 250 words required.")

    if len(algorithm_file) > 1:
        raise Exception(f"You have more than 1 file with extension ['pdf','docx','txt'] and we can only have 1. If you have readme files please make sure they don't have the same extention as one of those 3. I recommend .md for readme files. We use the presence of those extensions to identify which file is the algorithm description.")

    file_path = os.path.join(prediction_dir, algorithm_file[0])

    if file_path.find(".pdf") != -1:
        count_func = count_words_in_pdf
    elif file_path.find(".docx") != -1:
        count_func = count_words_in_docx
    elif file_path.find(".txt") != -1:
        count_func = count_words_in_txt
    else:
        raise Exception("Can't find a .pdf, .docx and .txt")


    total_words = count_func(file_path)
    pdb.set_trace()
    if total_words < 250:
        raise Exception(f"Total words less than 250 and we need more detail than that.")
    # elif total_words > 475:
    #     raise Exception(f"Total words more than 475 and we really want between 250 and 475.")

    print(f"We got your algorithm description and we see the total words in the PDF are: {total_words}.")
    


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
    # pdb.set_trace()

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
    # pdb.set_trace()
    auc_roc = roc_auc_score(y_true, y_score)
except:
    raise Exception("Can't compute auc_ROC for some reason")

# Confidence intervals
def confidence_interval_generation(y, x, confidence_interval_percent = 95):
    ## Confidence Interval
    n_bootstraps = 1000
    rng_seed = 42  # control reproducibility
    bootstrapped_scores = []
    rng = np.random.RandomState(rng_seed)
    for i in range(n_bootstraps):
        # bootstrap by sampling with replacement on the prediction indices
        indices = rng.randint(0, len(x), len(x))
        if len(np.unique(y[indices])) < 2:
            # We need at least one positive and one negative sample for ROC AUC
            # to be defined: reject the sample
            continue
        # score = metrics.cohen_kappa_score(y[indices], x[indices], weights="quadratic")
        score = roc_auc_score(y[indices], x[indices])
        bootstrapped_scores.append(score)
        # print("Bootstrap #{} ROC area: {:0.3f}".format(i + 1, score))
    # plt.hist(bootstrapped_scores, bins=50)
    # plt.title('Histogram of the bootstrapped ROC AUC scores')
    sorted_scores = np.array(bootstrapped_scores)
    sorted_scores.sort()
    # Computing the lower and upper bound of the 90% confidence interval
    # You can change the bounds percentiles to 0.025 and 0.975 to get
    # a 95% confidence interval instead.
    lower_percent = ((100-confidence_interval_percent)/2) / 100
    higher_percent = (100-(100-confidence_interval_percent)/2) / 100
    # pdb.set_trace()
    confidence_lower = sorted_scores[int(lower_percent * len(sorted_scores))]
    confidence_upper = sorted_scores[int(higher_percent * len(sorted_scores))]
    confidence_interval = "95% Confidence interval for the auc_roc: [{:0.3f} - {:0.3}]".format(confidence_lower, confidence_upper)
    # print(confidence_interval)
    return confidence_interval

auc_roc_confidence_interval = confidence_interval_generation(y_true, y_score)
## WLL
wll_list_df = pd.DataFrame([(wll,wll_list[wll]) for wll in wll_list.keys()], columns=['fileNamePath', 'wll'])
wll_list_df.sort_values('wll')
rows = wll_list_df.shape[0]
confidence_interval_percent = 95
lower_percent = ((100-confidence_interval_percent)/2) / 100
higher_percent = (100-(100-confidence_interval_percent)/2) / 100
confidence_lower = wll_list_df['wll'][int(lower_percent * rows)]
confidence_upper = wll_list_df['wll'][int(higher_percent * rows)]
confidence_95 = wll_list_df['wll'][int(lower_percent * rows):int(higher_percent * rows)]

import scipy
from scipy.stats import ttest_1samp
values = list(wll_list.values())
m = np.mean(values)
ttest = ttest_1samp(values, popmean=m)
# dir(ttest)
# ttest.confidence_interval()
# ttest.confidence_interval().low
# ttest.confidence_interval().high
# pdb.set_trace()

average_wll_95 = confidence_95.mean()
average_wll = np.mean(list(wll_list.values()))

## AUC_ROC
# print(f'Average Weighted Log Loss: {average_wll}')
# print(f'Average Weighted Log Loss 95% Confidence Interval: {average_wll_95}')
# print(f'AUC ROC: {auc_roc}')
# print(f'{auc_roc_confidence_interval}')

scores = {
    'average_wll': average_wll,
    'auc_roc': auc_roc
}

# detailed_scores = {f"{k} | wll -> ":wll_list[k] for k in wll_list.keys()}
detailed_scores = wll_list

with open(os.path.join(score_dir, 'scores.json'), 'w') as score_file:
    score_file.write(json.dumps(scores))
with open(os.path.join(score_dir, 'scores.html'), 'w') as html_file:
    html_file.write(f'<p>Average Weighted Log Loss: {average_wll}</p>\n')
    html_file.write(f'<p>Average Weighted Log Loss 95% Confidence Interval: {average_wll_95}</p>\n')
    html_file.write(f'<p>AUC ROC: {auc_roc}</p>\n')
    html_file.write(f'<p>{auc_roc_confidence_interval}</p>\n\n')
    html_file.write(f'<p>------------------------------------------------</p>\n')

    html_file.write(f"<p>Weighted Log Loss by Image:</p>\n")
    for key in detailed_scores:
        html_file.write(f"<p>{key} | {detailed_scores[key]}</p>\n")


