# Competition
# 

## reference data
zip -j reference_training_data.zip reference_data/training/*_IVIMParam.npy
zip -j reference_training_data.zip reference_data/training/*_TissueType.npy

zip -j reference_validation_data.zip reference_data/validation/organizer/*_IVIMParam.npy
zip -j reference_validation_data.zip reference_data/validation/organizer/*_TissueType.npy

zip -j reference_testing_data.zip reference_data/testing/organizer/*_IVIMParam.npy
zip -j reference_testing_data.zip reference_data/testing/organizer/*_TissueType.npy

## public data
zip -j public_training_data.zip public_data/training/*
zip -j public_validation_data.zip public_data/validation/*
zip -j public_testing_data.zip public_data/testing/*

## Bundle
### Folders (can do zips but why? haha.)
zip -r ivim_challenge_bundle_folders.zip \
  reference_data \
  starting_kit \
  public_data \
  input_data \
  ingestion_program \
  scoring_program;

zip -j ivim_challenge_bundle_folders.zip \
  competition.yaml \
  data.md \
  get_started.md \
  evaluation.md \
  overview.md \
  how_the_challenge_works.md \
  terms.md \
  logo.jpg;


# Sample training submission

cd sample_submission;
zip -r sample_submission.zip ./*;
cp sample_submission.zip ../;
rm sample_submission.zip
cd ../

# Sample Run

## Docker
cd scoring_program;
docker build -t codalab/codalab-legacy:py37BB .;
docker tag codalab/codalab-legacy:py37BB bbearce/codalab-legacy:ivim
cd ../
# docker push bbearce/codalab-legacy:ivim

## We work with example and copy working version to scoring_program to be zipped
## DO NOT DO THE OPPOSITE OR YOU OVERWRITE YOUR WORKING COPY WITH AN OLD ONE

export input="input"
export program="program"
export output="output"
export command="bash"
export command="python $program/score.py $input $output"
docker run \
    -it \
    --rm \
    -e input=input \
    -e output=output \
    -e program=program \
    -v "/sddata/projects/Challenges/IVIM/submission_directory":"/app" \
    -w "/app" \
    codalab/codalab-legacy:py37BB $command


## Python

input=submission_directory/input
output=submission_directory/output
program=submission_directory/program
python $program/score.py $input $output


## scoring program
cp -r submission_directory/program/* scoring_program/
rm scoring_program.zip
zip -j scoring_program.zip scoring_program/*
