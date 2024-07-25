# How to participate

There are two parts two a submission, ingestion and scoring. 

## Ingestion Program:

This takes the code you (participant) define and runs it against our input data.

* ingestion - challenge organizer program
* ingested - participant provided algorithm

```bash
ROOT=/sddata/projects/Challenges/XAI
cd $ROOT
```

System execution:
```bash
DOCKER_IMAGE="codalab/codalab-legacy:py37"
# COMMAND="python3 /app/program/ingestion.py /app/input_data/ /app/output/ /app/program /app/ingested_program" # Normal Run
COMMAND="python3 /app/ingested_program/main.py /app/input_data/ /app/output/ /app/program /app/ingested_program"
DIR_OF_RUN="$ROOT/app_ingestion" # "/app" in container

docker run \
  --rm \
  --name=test_run \
  --security-opt=no-new-privileges \
  -v $DIR_OF_RUN/ingestion_program:/app/program \
  -v $DIR_OF_RUN/output:/app/output \
  -w /app/program \
  -e PYTHONUNBUFFERED=1 \
  -v $DIR_OF_RUN/program:/app/ingested_program \
  -v $DIR_OF_RUN/input_data:/app/input_data \
  -it \
  $DOCKER_IMAGE $COMMAND
  # -it bash
```

> Note -v is defined as: ```-v <local VM dir of run>:<container dir>```

### Docker Image
* `DOCKER_IMAGE="codalab/codalab-legacy:py37"`

This is the docker image you upload.

### Command
Command run on the backend:

* COMMAND=`python3 /app/program/ingestion.py /app/input_data/ /app/output/ /app/program /app/ingested_program`
* `/app` is the location in the container where the root of a *submission* lives.
* Folder structure in container:
```
/app
  - program/ -> from "ingestion_program" and we define this to consume your model\algorithm
    * ingestion.py
  - input_data/ - source data
    * testing_data
    * training_data
    * training_label
  - output/ - predictions
    * metadata.json
    * prediction
  - ingested_program -> from "program" and is your algorithm
    * model.py
```

`/app/ingested_program` **is what your are responsible for**:
```python
class Model:
    def fit(self, X_train, y_train):
        """
        This should handle the logic of training your model
        :param X_train: 7 dimensional np.array of training data
        :param y_train: 1 dimensional np.array of the same length as X_train. Contains classifications of X_train
        """
        pass

    def predict(self, X_test):
        """
        This should handle making predictions with a trained model
        :param X_test: 7 dimensional np.array of testing data
        :return: 1 dimensional np.array of the same length as X_test containing predictions to each point in X_test
        """
        pass
```
Ex:
```python
from sklearn.cluster import KMeans

class Model:
    def __init__(self):
        self.kmeans = KMeans(n_clusters=3)

    def fit(self, X, y):
        self.kmeans.fit(X=X, y=y)

    def predict(self, X):
        return self.kmeans.predict(X)
```

`/app/program/ingestion.py` **is what runs your code**:
```python
import json
import os
import sys
import time

import numpy as np

# Data that can't be seen except by participant algorithm while running, and is input to their algorithm
input_dir = os.path.abspath(sys.argv[1]) # /app/input_data/

# When ingestion, this is the predictions folder
output_dir = os.path.abspath(sys.argv[2]) # /app/output/

# When ingestion, this is the ingestion program folder
# Available here in case extra utils are needed
program_dir = os.path.abspath(sys.argv[3]) # /app/program

# When ingestion, this is the ingested program (YOU ARE RESPONSIBLE FOR THIS)
submission_dir = os.path.abspath(sys.argv[4]) # /app/ingested_program

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

```


## Score:

Prep `app_scoring` directory with participant predictions:
```bash
cp $ROOT/app_ingestion/output/* $ROOT/app_scoring/input/res/
```

System Execution:
```bash
DOCKER_IMAGE="codalab/codalab-legacy:py37"
COMMAND="python3 /app/program/scoring.py /app/input/ /app/output/"
DIR_OF_RUN="$ROOT/app_scoring" # "/app" in container

docker run \
  --rm \
  --name=test_run \
  --security-opt=no-new-privileges \
  -v $DIR_OF_RUN/program:/app/program \
  -v $DIR_OF_RUN/output:/app/output \
  -w /app/program \
  -e PYTHONUNBUFFERED=1 \
  -v $DIR_OF_RUN/input:/app/input \
  -it \
  $DOCKER_IMAGE $COMMAND
```

Command run on the backend:

```bash
command: python3 /app/program/scoring.py /app/input/ /app/output/
```

Folder structure:
> `input_data` is now `input`
```
/app
  - program
    * scoring.py -> Challenge organizers design
  - input/
    * res/ -> this is the predictions from before and was "output" in the ingestion section
      - metadata.json
      - prediction
    * ref/
      - testing_label -> secret label to compare predictions to
  - output/ -> Now is scoring metrics output
```

## Build Docker Image

```bash
# Test build
docker build -f ./sample_docker_image/Dockerfile -t qtimchallenges.azurecr.io/user_1:py37 ./sample_docker_image

cd sample_docker_image 
zip sample_docker_image.zip ./*
```