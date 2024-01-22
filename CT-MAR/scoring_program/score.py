#!/usr/bin/env python
import sys
import os, pdb
import os.path
import time
import math
import cv2
import json
import numpy as np

input_dir = sys.argv[1]
output_dir = sys.argv[2]

submit_dir = os.path.join(input_dir, 'res')
truth_dir = os.path.join(input_dir, 'ref')

if not os.path.isdir(submit_dir):
    print (f"{submit_dir} doesn't exist")

def compute_metrics(refImages, participantImages):
    # Structural Similarity
    ss = [1 for i in range(len(refImages))]
    # RMSE
    # mse = np.square(np.subtract(y_actual,y_predicted)).mean()
    rmse = []
    for (r_img, p_img) in zip(refImages, participantImages):
        ref_image = cv2.imread(os.path.join(truth_dir, r_img))
        participant_image = cv2.imread(os.path.join(submit_dir, p_img))
        try:
            mse = np.square(np.subtract(ref_image,participant_image)).mean()
        except:
            print("ref")
            print(refImages)
            print("par")
            print(participantImages)
        rmse.append(math.sqrt(mse))
    # Spatial Resolution
    sr = [1 for i in range(len(refImages))]
    # Noise
    n = [1 for i in range(len(refImages))]
    # Lesion Detectability
    ld = [1 for i in range(len(refImages))]
    # Feature Dimension Accuracy
    fda = [1 for i in range(len(refImages))]
    # Residual Streak Amplitude
    rsa = [1 for i in range(len(refImages))]
    metrics = {
        'ss': ss,
        'rmse': rmse,
        'sr': sr,
        'n': n,
        'ld': ld,
        'fda': fda,
        'rsa': rsa
    }

    # Calculate Score
    C = len(refImages) # num cases
    weights = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    internal_sum = 0
    for case_index in range(C):
        for metric_index, m in enumerate(metrics.keys()):
            weight_for_metric = weights[metric_index]
            internal_sum += weight_for_metric * metrics[m][case_index]
    # S is final Score
    S = internal_sum / C
    # pdb.set_trace()

    return S, metrics


if os.path.isdir(submit_dir) and os.path.isdir(truth_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, 'scores.txt')
    output_file = open(output_filename, 'w')
    
    html_filename = os.path.join(output_dir, 'scores.html')
    html_file = open(html_filename, 'w')

    # Participant Data    
    ref_images = os.listdir(truth_dir)
    participant_images = os.listdir(submit_dir)
    S, metrics = compute_metrics(refImages = ref_images, participantImages = participant_images)
    # pdb.set_trace()

    if S is not None and metrics is not None:
        output_file.write(f"Score: {S}")
        html_file.write(json.dumps(metrics, indent=2))
    else:
        if S is not None:
            output_file.write(b"Score: 0")
        else:
            raise Exception("There is some error with obtaining Score")
        if metrics is not None:
            html_file.write(json.dumps(metrics, indent=2))

    output_file.close()
    html_file.close()
