# How to participate

1. Create your own Dockerfile (and related files for build), zip and upload to our system or use our default one we provide. 
  * You will have a drop down to select the docker image you want your code to run in.
  * This is a *.zip archive with a `Dockerfile` file at the **root** of the archive.
  * The Dockerfile you submit does not need to have a CMD or ENTRYPOINT
instruction, and does not need to mount drives or copy your submitted
application.  All of that will be handled by the administrative wrapper
(ingestion) software that is run at the challenge site.
  * If creating your own Dockerfile, it should download or
provide whatever packages or other tools that your inference software
needs.
  * A sample is provided in the starting kit your are perusing.
2. Upload a submission ZIP file, which will have your inference software (such as a "main.py" file), any other files your software needs (such as a model file), and an "entrypoint.sh" file that the administrative wrapper (ingestion) program will call, that should in turn run your application. This shell script will be called by our platform with input arguments:
  * input arguments:
    - /app/input_data/
    - /app/output/
    - /app/ingested_program/
  * A sample is provided in starting_kit/app_ingestion/program


## Entrypoint.sh

Your "entrypoint.sh" script, which will be called by the administrative
wrapper (ingestion) script at the challenge site, should be a Bash script
that calls your inference application.  As indicated in the comments of
the example script below, it should expect (and pass along) three arguments:

  1. The input directory that will contain the DICOM images that your
application should perform inference on;
  2. The output directory where your application should put its inference
output (as per challenge instructions); and
  3. The submission directory where your application (all contents of your
submission ZIP file, including entrypoint.sh) resides.

## Main.py

In our example, the "entrypoint.sh" script calls our "main.py" that we
have submitted.  The "main.py" script takes the same three arguments that
the "entrypoint.sh" script takes:  the data input directory, the data
output directory, and the submission directory (ingested_program) where
all of the contents of the submission zip file have been placed.


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
  --gpus all \
  --runtime=nvidia \
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
cp $ROOT/app_ingestion/output/image-level-classifications.csv $ROOT/app_scoring/input/res/
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
