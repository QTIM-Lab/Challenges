# How to participate

1. Build your own docker image and upload to our system or use our default one we provide. 
  * You will have a drop down to select the docker image you want your code to run in.
  * This is a *.zip archive with a `Dockerfile` file at the **root** of the archive.
2. Upload another zip with your algorith inside it with `entrypoint.sh` in it. This shell script will be called by our platform with input argumentss:
  * /app/input_data/
  * /app/output/
  * /app/ingested_program/

```bash
bash /app/ingested_program/entrypoint.sh /app/input_data/ /app/output/ /app/ingested_program/
```

## Set Working Directory
```bash
ROOT=. # Dir of starting_kit; If cwd is inside `starting_kit`, "./" is perfect.
cd $ROOT
```

## Build Docker Image

```bash
# Example build
docker build -f ./sample_docker_image/Dockerfile -t repo/xai-challenge:demo-score  ./sample_docker_image

cd sample_docker_image 
zip sample_docker_image.zip ./*
```

> Now upload your image



There are two parts to the submission process. The ingestion and scoring portion. You are only responsible for the ingestion portion. We then score your predictions in the scoring section. 



## Ingestion Program:

Our code takes the code you (participant) define and runs it against our input data (chest xrays).

How the system executes your submission:
```bash
# This is your built image or our default
DOCKER_IMAGE="repo/xai-challenge:demo-score"
# We run your /app/ingested_program/entrypoint.sh file with inputs that that are paths to the input dicoms and a place for your output as well as access to your code directory.
COMMAND="bash /app/ingested_program/entrypoint.sh /app/input_data/ /app/output/ /app/ingested_program/"
DIR_OF_RUN="$ROOT/app_ingestion" # "/app" in container

# Sample run on platform that you can simulate locally.
# Directories on the right side of : in the -v arguments are what is available inside the running container.
docker run \
  --rm \
  --name=test_run \
  --security-opt=no-new-privileges \
  -v $DIR_OF_RUN/input_data:/app/input_data \
  -v $DIR_OF_RUN/output:/app/output \
  -v $DIR_OF_RUN/program:/app/ingested_program \
  -v $DIR_OF_RUN/ingestion_program:/app/program \
  -w /app/program \
  -e PYTHONUNBUFFERED=1 \
  $DOCKER_IMAGE $COMMAND
```

> Note -v is defined as: ```-v <local VM dir of run>:<container dir>```

* `/app` is the location in the container where the root of a *submission* lives.
* Folder structure **in** container:
```
/app
  - program/ - we define this to consume your model\algorithm. Holds $COMMAND from above
    * metadata.yaml - contains $COMMAND above
  - input_data/ - source data
    * This is where source *.dcm images will be located
  - output/ - predictions we expect
    * <dicom-file-name>.png
    * <dicom-file-name>.png
    * <dicom-file-name>...
    * image-level-classifications.csv # must have this name
  - ingested_program - from "program" and is your algorithm
    * entrypoint.sh - **MUST HAVE** and calls optional other files
    * ...optional other files
```


## Scoring Program:

> Note: You don't need to know this, but is here if it helps the whole process make more sense.

Prep the `app_scoring` directory with participant predictions we just made:
> Note: the "/app/input" dir means data as input to scoring program
```bash
cp $ROOT/app_ingestion/output/*.png $ROOT/app_scoring/input/res/
```

How the system scores your submission:
```bash
DOCKER_IMAGE="repo/xai-challenge:demo-score"
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
