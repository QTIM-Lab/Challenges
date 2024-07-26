# How to participate

## Build Docker Image

```bash
# Test build
docker build -f ./sample_docker_image/Dockerfile -t demo_image/user_1:py37 ./sample_docker_image

cd sample_docker_image 
zip sample_docker_image.zip ./*
```

> Now upload your image



There are two parts to a submission. The ingestion and scoring portion. You are only responsible for the ingestion portion. We then score your predictions in the scoring section. 



## Ingestion Program:

This takes the code you (participant) define and runs it against our input data (chest xrays).

* ingestion - challenge organizer program
* ingested - participant provided algorithm

```bash
# ROOT=./ # Dir of starting_kit; If inside "./" is perfect.
ROOT=/sddata/projects/Challenges/XAI # Dir of starting_kit; If inside "./" is perfect.
cd $ROOT
```

How the system executes your submission:
```bash
# This is your built image or our default
DOCKER_IMAGE="demo_image/user_1:py37"
# We run your /app/ingested_program/main.py file with inputs that give access to the input dicoms and a place for your output.
# Only worry about `/app/input_data/` and `/app/output/`. The rest are for us (organizers):  `/app/program` and `/app/ingested_program`.
COMMAND="python3 /app/ingested_program/main.py /app/input_data/ /app/output/ /app/program /app/ingested_program"
DIR_OF_RUN="$ROOT/app_ingestion" # "/app" in container

# Technically we run this but notice `/app/input_data/` and `/app/output/` are available make our locally available directories accessible to you.
# Directories on the right side of : in the -v arguments are what is available inside the running container.
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

Command run on the backend:
* COMMAND=`python3 /app/ingested_program/main.py /app/input_data/ /app/output/ /app/program /app/ingested_program`
* `/app` is the location in the container where the root of a *submission* lives.
* Folder structure **in** container:
```
/app
  - program/ - from "ingestion_program" and we define this to consume your model\algorithm
    * metadata.yaml - contains COMMAND above
  - input_data/ - source data
    * This is where source *.dcm images will be located
  - output/ - predictions we expect
    * *.npy
    * *.npy
    * *...
    * image-level-classifications.csv
  - ingested_program - from "program" and is your algorithm
    * main.py - We need this to be named `main.py` so the COMMAND above to work
    * ...optional other files
```

`/app/ingested_program` **is what your are responsible for**


## Scoring Program:

Prep the `app_scoring` directory with participant predictions we just made:
```bash
cp $ROOT/app_ingestion/output/* $ROOT/app_scoring/input/res/
```

How the system scores your submission:
```bash
DOCKER_IMAGE="demo_image/user_1:py37"
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
    * scoring.py - Challenge organizers design
    * metadata.yaml - contains execution command for scoring program (don't worry about this)
  - input/
    * res/ -> this is the predictions from before and was "output" in the ingestion section
      - *.npy
      - *.npy
      - *...
      - image-level-classifications.csv
    * ref/ -> this is our reference
      -
  - output/ -> This is scoring metrics output
```
