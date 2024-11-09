# IVIM Challenge
```bash
shopt -s extglob # This command enables the extended pattern matching features in Bash, allowing us to use `!(pattern)` to match everything except the specified pattern.
```

```bash
ROOT=/sddata/projects/Challenges/IVIM
cd $ROOT
DATA=/sddata/data/Challenges/IVIM
```

## Submission Dir
This is the structure the compute worker sees while running and the universe you are in when a participant uploads a submission. It is built in `/tmp/codabench/tmp#######` during a run and mounted into a docker container with `-v`.

`-v /tmp/codabench/tmp#######:/app` (located at `$ROOT/submission_directory` in git repo):
> /app is $ROOT/submission_directory
```bash
/submission_directory 
  /input # Called input as it is input to scoring program.
    /ref # Ground truth known as reference_data.
    /res # Participant results. Contains contents of their submitted *.zip archive during a submission run
  /output # results.txt and resuls.html and is scoring program output.
  /program # Contains the scoring program.
```

> In each section there is a place where we copy the ref data, submission or program to the submission_directory

## Ground Truth
Retrieve from `$DATA`.

Data has been split up as follows:
`/sddata/data/Challenges/IVIM/raw_phase_data_from_organizers`: 
  * train
  * val
  * test

From here 2 subsets were made with the same layout:  
### Public (will be shared with participants)
* `/sddata/data/Challenges/IVIM/public_data`:
  * train
  * val
  * test
### Reference (used to grade submissions - private)
* `/sddata/data/Challenges/IVIM/reference_data`:
  * train
  * val
  * test

> Bottom of file has raw bash that does the splitting

## Reference Data
```bash
ROOT=/sddata/projects/Challenges/IVIM
cd $ROOT
DATA=/sddata/data/Challenges/IVIM
# Which phase
PHASE=train
PHASE=test
PHASE=val
PHASE=val_10
# Extract raw data
unzip $DATA/reference_"$PHASE"_data.zip -d $ROOT/submission_directory/input/ref
# Re-compress
cd $ROOT/submission_directory/input/ref
zip -r reference_"$PHASE"_data.zip ./*; mv reference_"$PHASE"_data.zip $DATA/;
cd $ROOT
# To clean
rm -r $ROOT/submission_directory/input/ref/!(.gitkeep) # leave .gitkeep so we can keep this in git

# Don't need this anymore but keeping around for challenge duration just in case:
## $DATA/archive/reference_data
## $DATA/archive/public_data
```

## Public Data
```bash
ROOT=/sddata/projects/Challenges/IVIM
cd $ROOT
DATA=/sddata/data/Challenges/IVIM
# Which phase
PHASE=train
PHASE=test
PHASE=val
PHASE=val_10
# Extract raw data
unzip $DATA/public_"$PHASE"_data.zip -d $DATA/public_"$PHASE"_data
# Re-compress
cd $DATA/public_"$PHASE"_data
zip -r public_"$PHASE"_data.zip ./*; mv public_"$PHASE"_data.zip $DATA/;
cd $ROOT
# To clean
rm -r $DATA/public_"$PHASE"_data
```


## Sample Submissions
Retrieve from `$DATA`.
```bash
ROOT=/sddata/projects/Challenges/IVIM
cd $ROOT
DATA=/sddata/data/Challenges/IVIM
# Which phase
# PHASE=train # we skipped because it is big
PHASE=val
PHASE=val_10
PHASE=test
# Extract raw data
unzip $DATA/sample_"$PHASE"_submission.zip -d $ROOT/submission_directory/input/res/
# Re-compress
cd $DATA/sample_"$PHASE"_submission
zip -r sample_"$PHASE"_submission.zip ./*; mv sample_"$PHASE"_submission.zip $DATA/; cd $ROOT
# Clean up
rm -r $ROOT/submission_directory/input/res/!(.gitkeep) # leave .gitkeep so we can keep this in git
```


## Scoring Program
Retrieve from `$DATA`.
```bash
ROOT=/sddata/projects/Challenges/IVIM
cd $ROOT
DATA=/sddata/data/Challenges/IVIM
# Which phase
PHASE=val
PHASE=test
# Extract raw data
unzip $DATA/scoring_"$PHASE"_program.zip -d $ROOT/submission_directory/program/
# Re-compress
cd $ROOT/submission_directory/program
zip -r scoring_"$PHASE"_program.zip ./*; mv scoring_"$PHASE"_program.zip $DATA/; cd $ROOT
# Clean up
rm -r $ROOT/submission_directory/program/!(.gitkeep) # leave .gitkeep so we can keep this in git
```


## Starting Kit
Retrieve from `$DATA`.
```bash
ROOT=/sddata/projects/Challenges/IVIM
cd $ROOT
DATA=/sddata/data/Challenges/IVIM
# Which phase
PHASE=train
# Extract raw data
unzip $DATA/"$PHASE"_starting_kit.zip -d $DATA/"$PHASE"_starting_kit
# Re-compress
cd $DATA/"$PHASE"_starting_kit
zip -r "$PHASE"_starting_kit.zip ./*; mv "$PHASE"_starting_kit.zip $DATA/; cd $ROOT
# Clean up
rm -r $DATA/"$PHASE"_starting_kit/
```


## Output
```bash
rm -r $ROOT/submission_directory/output/!(.gitkeep) # leave .gitkeep so we can keep this in git
```


## Sample Run
### Python
```bash
cd $ROOT
input=submission_directory/input
output=submission_directory/output
program=submission_directory/program
python $program/score.py $input $output
```

### Docker
```bash
cd scoring_program;
docker build -t codalab/codalab-legacy:py37BB .;
docker tag codalab/codalab-legacy:py37BB bbearce/codalab-legacy:ivim
cd ../
docker push bbearce/codalab-legacy:ivim
```

Run like the platform will run:
```bash
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
    codalab/codalab-legacy:ivim $command
```


## Bundle
### Folders
> We use two sesparate commands but contents show up in the same file

```bash
ROOT=/sddata/projects/Challenges/IVIM
cd $ROOT
DATA=/sddata/data/Challenges/IVIM

cp $DATA/reference_train_data.zip $ROOT/
cp $DATA/reference_val_data.zip $ROOT/
cp $DATA/reference_test_data.zip $ROOT/
cp $DATA/public_train_data.zip $ROOT/
cp $DATA/public_val_data.zip $ROOT/
cp $DATA/public_test_data.zip $ROOT/
cp $DATA/scoring_val_program.zip $ROOT/
cp $DATA/train_starting_kit.zip $ROOT/

zip -j ivim_challenge_bundle.zip \
  competition.yaml \
  data.md \
  get_started.md \
  evaluation.md \
  overview.md \
  how_the_challenge_works.md \
  terms.md \
  logo.jpg \
  reference_train_data.zip \
  reference_val_data.zip \
  reference_test_data.zip \
  public_train_data.zip \
  public_val_data.zip \
  public_test_data.zip \
  train_starting_kit.zip \
  scoring_val_program;


# rm $ROOT/reference_train_data.zip
# rm $ROOT/reference_val_data.zip
# rm $ROOT/reference_test_data.zip
# rm $ROOT/public_train_data.zip
# rm $ROOT/public_val_data.zip
# rm $ROOT/public_test_data.zip
# rm $ROOT/scoring_val_program.zip
# rm $ROOT/train_starting_kit.zip

mv /sddata/projects/Challenges/IVIM/ivim_challenge_bundle.zip /sddata/data/Challenges/IVIM/archive/
```



## Files needed
### Organizer files
 *_gtDWIs.npy - raw ground truth image...not used
 *_IVIMParam.npy - actual ground truth
 *_TissueType.npy - Tissue types used with noisy kspace image
### User files
 *_NoisyDWIK.npy - noisy k-space image given to participants

### Raw Data (BE CAREFUL)
#### Training
```bash
ROOT_DATA_DIR=/sddata/data/Challenges/IVIM
```

```bash
# REF
cp -r $ROOT_DATA_DIR/raw_phase_data_from_organizers/train/*_IVIMParam.npy $ROOT_DATA_DIR/reference_data/training/
cp -r $ROOT_DATA_DIR/raw_phase_data_from_organizers/train/*_TissueType.npy $ROOT_DATA_DIR/reference_data/training/
# PUB (During this phase they are allowed to see more)
cp -r $ROOT_DATA_DIR/raw_phase_data_from_organizers/train/*_gtDWIs.npy $ROOT_DATA_DIR/public_data/training/
cp -r $ROOT_DATA_DIR/raw_phase_data_from_organizers/train/*_IVIMParam.npy $ROOT_DATA_DIR/public_data/training/
cp -r $ROOT_DATA_DIR/raw_phase_data_from_organizers/train/*_TissueType.npy $ROOT_DATA_DIR/public_data/training/
cp -r $ROOT_DATA_DIR/raw_phase_data_from_organizers/train/*_NoisyDWIk.npy $ROOT_DATA_DIR/public_data/training/
```

#### Validation
```bash
# REF
cp -r $ROOT_DATA_DIR/raw_phase_data_from_organizers/validate/organizer/*_IVIMParam.npy $ROOT_DATA_DIR/reference_data/validation/
cp -r $ROOT_DATA_DIR/raw_phase_data_from_organizers/validate/organizer/*_TissueType.npy $ROOT_DATA_DIR/reference_data/validation/
# PUB
cp -r $ROOT_DATA_DIR/raw_phase_data_from_organizers/validate/user/*_NoisyDWIk.npy $ROOT_DATA_DIR/public_data/validation/
```

#### Testing
```bash
# REF
cp -r $ROOT_DATA_DIR/raw_phase_data_from_organizers/test/organizer/*_IVIMParam.npy $ROOT_DATA_DIR/reference_data/testing/
cp -r $ROOT_DATA_DIR/raw_phase_data_from_organizers/test/organizer/*_TissueType.npy $ROOT_DATA_DIR/reference_data/testing/
# PUB
cp -r $ROOT_DATA_DIR/raw_phase_data_from_organizers/test/user/*_NoisyDWIk.npy $ROOT_DATA_DIR/public_data/testing/
```
