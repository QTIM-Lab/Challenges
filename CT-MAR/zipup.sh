# Ground Truths
cp -r /sddata/projects/Challenges/CT-MAR/reference_data /sddata/data/Challenges/CT-MAR/
zip -j reference_data.zip reference_data/*

# Public Data
zip -j public_data.zip public_data/*

# Scoring Program
zip -j scoring_program.zip scoring_program/*

# Starting Kit
zip -j starting_kit.zip starting_kit/*

# Bundle
zip -j ct_mar_challenge_bundle.zip \
  competition.yaml \
  challenge-data.md \
  get-started.md \
  how-the-challenge-works.md \
  important-dates.md \
  objective.md \
  organizers.md \
  overview.md \
  results-prizes-and-publication-plan.md \
  scoring-metrics.md \
  terms.md \
  CT-MARLogo.png \
  reference_data.zip \
  starting_kit.zip \
  public_data_training.zip \
  public_data_validation.zip \
  scoring_program.zip

# [5] Sample training submission
cp -r /sddata/projects/Challenges/CT-MAR/sample_submission /sddata/data/Challenges/CT-MAR/
cd sample_submission;
zip -r sample_submission.zip ./*;
cp sample_submission.zip ../;
rm sample_submission.zip
cd ../

# [6] Sample Run
## Docker
cd scoring_program;
docker build -t codalab/codalab-legacy:py37BB .;
docker tag codalab/codalab-legacy:py37BB bbearce/codalab-legacy:ct-mar
docker push bbearce/codalab-legacy:ct-mar
rm -rf /tmp/submission_directory/;
cp -r submission_directory /tmp/;

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
    -v "/tmp/submission_directory":"/tmp/submission_directory" \
    -w "/tmp/submission_directory" \
    codalab/codalab-legacy:py37BB $command


## Python
input=submission_directory/input
output=submission_directory/output
program=submission_directory/program
python $program/score.py $input $output

ls /tmp/
ls /tmp/submission_directory/
ls /tmp/submission_directory/output
cat /tmp/submission_directory/output/scores.txt
cat /tmp/submission_directory/output/scores.html

cp /tmp/submission_directory/output/scores.txt submission_directory/output/
cp /tmp/submission_directory/output/scores.html submission_directory/output/

vi /tmp/submission_directory/output/scores.html
