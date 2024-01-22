# Competition

## Files needed
### Organizer files
# *_gtDWIs.npy - raw ground truth image...not used
# *_IVIMParam.npy - actual ground truth
# *_TissueType.npy - Tissue types used with noisy kspace image
### User files
# *_NoisyDWIK.npy - noisy k-space image given to participants

## Moving data to and from /sddata/data/Challenges 
### Clear current working area
# rm /sddata/projects/Challenges/IVIM/reference_data/training/*
# rm /sddata/projects/Challenges/IVIM/reference_data/validation/*
# rm /sddata/projects/Challenges/IVIM/reference_data/testing/*
# rm /sddata/projects/Challenges/IVIM/public_data/training/*
# rm /sddata/projects/Challenges/IVIM/public_data/validation/*
# rm /sddata/projects/Challenges/IVIM/public_data/testing/*

### From /sddata/data
#### Training
cp -r /sddata/data/Challenges/IVIM/phase_data/train/*_IVIMParam.npy /sddata/projects/Challenges/IVIM/reference_data/training/
cp -r /sddata/data/Challenges/IVIM/phase_data/train/*_TissueType.npy /sddata/projects/Challenges/IVIM/reference_data/training/

cp -r /sddata/data/Challenges/IVIM/phase_data/train/*_gtDWIs.npy /sddata/projects/Challenges/IVIM/public_data/training/
cp -r /sddata/data/Challenges/IVIM/phase_data/train/*_IVIMParam.npy /sddata/projects/Challenges/IVIM/public_data/training/
cp -r /sddata/data/Challenges/IVIM/phase_data/train/*_TissueType.npy /sddata/projects/Challenges/IVIM/public_data/training/
cp -r /sddata/data/Challenges/IVIM/phase_data/train/*_NoisyDWIk.npy /sddata/projects/Challenges/IVIM/public_data/training/

#### Validation
cp -r /sddata/data/Challenges/IVIM/phase_data/validate/organizer/*_IVIMParam.npy /sddata/projects/Challenges/IVIM/reference_data/validation/
cp -r /sddata/data/Challenges/IVIM/phase_data/validate/organizer/*_TissueType.npy /sddata/projects/Challenges/IVIM/reference_data/validation/

cp -r /sddata/data/Challenges/IVIM/phase_data/validate/user/*_NoisyDWIk.npy /sddata/projects/Challenges/IVIM/public_data/validation/

#### Testing
cp -r /sddata/data/Challenges/IVIM/phase_data/test/organizer/*_IVIMParam.npy /sddata/projects/Challenges/IVIM/reference_data/testing/
cp -r /sddata/data/Challenges/IVIM/phase_data/test/organizer/*_TissueType.npy /sddata/projects/Challenges/IVIM/reference_data/testing/

cp -r /sddata/data/Challenges/IVIM/phase_data/test/user/*_NoisyDWIk.npy /sddata/projects/Challenges/IVIM/public_data/testing/


### From /sddata/projects
# cp -r /sddata/projects/Challenges/IVIM/reference_data/training/*_gtDWIs.npy /sddata/data/Challenges/IVIM/phase_data/train/
# cp -r /sddata/projects/Challenges/IVIM/reference_data/training/*_IVIMParam.npy /sddata/data/Challenges/IVIM/phase_data/train/
# cp -r /sddata/projects/Challenges/IVIM/reference_data/training/*_TissueType.npy /sddata/data/Challenges/IVIM/phase_data/train/
# cp -r /sddata/projects/Challenges/IVIM/reference_data/training/*_NoisyDWIk.npy /sddata/data/Challenges/IVIM/phase_data/train/

# cp -r /sddata/projects/Challenges/IVIM/reference_data/validate/organizer/*_gtDWIs.npy /sddata/data/Challenges/IVIM/phase_data/train/organizer/
# cp -r /sddata/projects/Challenges/IVIM/reference_data/validate/organizer/*_IVIMParam.npy /sddata/data/Challenges/IVIM/phase_data/train/organizer/
# cp -r /sddata/projects/Challenges/IVIM/reference_data/validate/organizer/*_TissueType.npy /sddata/data/Challenges/IVIM/phase_data/train/organizer/
# cp -r /sddata/projects/Challenges/IVIM/reference_data/validate/user/*_NoisyDWIk.npy /sddata/data/Challenges/IVIM/phase_data/train/user/

# cp -r /sddata/projects/Challenges/IVIM/reference_data/test/organizer/*_gtDWIs.npy /sddata/data/Challenges/IVIM/phase_data/train/organizer/
# cp -r /sddata/projects/Challenges/IVIM/reference_data/test/organizer/*_IVIMParam.npy /sddata/data/Challenges/IVIM/phase_data/train/organizer/
# cp -r /sddata/projects/Challenges/IVIM/reference_data/test/organizer/*_TissueType.npy /sddata/data/Challenges/IVIM/phase_data/train/organizer/
# cp -r /sddata/projects/Challenges/IVIM/reference_data/test/user/*_NoisyDWIk.npy /sddata/data/Challenges/IVIM/phase_data/train/user/

## Starting Kit
zip -j starting_kit.zip starting_kit/*

## reference data
### training
zip -j reference_training_data.zip reference_data/training/*

### validation
zip -j reference_validation_data.zip reference_data/validation/*

### testing
zip -j reference_testing_data.zip reference_data/testing/*

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
ls sample_submission
rm ./sample_submission/*
cp /sddata/data/Challenges/IVIM/phase_data/train/*_IVIMParam.npy ./sample_submission/
zip -j sample_submission.zip ./sample_submission/*;
rm sample_submission.zip

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