import json
import os
import sys
import time

import numpy as np

# Data that can't be seen except by participant algorithm and is input to their algorithm
input_dir = os.path.abspath(sys.argv[1]) # /app/input_data/

# When ingestion, this is the predictions folder
output_dir = os.path.abspath(sys.argv[2]) # /app/output/

# When ingestion, this is the ingestion program (we are looking at the file in this directory)
# Available here in case extra utils are needed
program_dir = os.path.abspath(sys.argv[3]) # /app/program

# When ingestion, this is the ingested program (YOU ARE RESPONSIBLE FOR THIS)
submission_dir = os.path.abspath(sys.argv[4]) # /app/ingestion_program

sys.path.append(program_dir) # Allow the loading of any extra utils
sys.path.append(submission_dir) # Allow the loading of participant's code


def get_training_data():
    X_train = np.genfromtxt(os.path.join(input_dir, 'training_data'))
    y_train = np.genfromtxt(os.path.join(input_dir, 'training_label'))
    return X_train, y_train


def get_prediction_data():
    return np.genfromtxt(os.path.join(input_dir, 'testing_data'))


def main():
    # LOAD PARTICIPANT CODE
    from model import Model
    print('Reading Data')
    X_train, y_train = get_training_data()
    X_test = get_prediction_data()
    print('Starting')
    start = time.time()
    m = Model()
    print('Training Model')
    m.fit(X_train, y_train)
    print('Running Prediction')
    prediction = m.predict(X_test)
    duration = time.time() - start
    print(f'Completed Prediction. Total duration: {duration}')
    np.savetxt(os.path.join(output_dir, 'prediction'), prediction)
    with open(os.path.join(output_dir, 'metadata.json'), 'w+') as f:
        json.dump({'duration': duration}, f)


if __name__ == '__main__':
    main()
