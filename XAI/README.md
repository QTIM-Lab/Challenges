# Code Submission Challenge Template

> Upasana, I'm shifting things as I go but below is sort of the general scripts to clear data out and restore it. Look at "how_to_submit.md" for direct instructions and explaination of ingestion\scoring program.

```bash
shopt -s extglob # This command enables the extended pattern matching features in Bash, allowing us to use `!(pattern)` to match everything except the specified pattern.
```
```bash
ROOT=/sddata/projects/Challenges/XAI
cd $ROOT
DATA=/sddata/data/Challenges/XAI
```

## Create Bundle
```bash
# rm xai_code_submission_template_bundle.zip
zip -r xai_code_submission_template_bundle.zip ./*
```


## Backup Bundle
```bash
cp $ROOT/xai_code_submission_template_bundle.zip $DATA/
```


## Create Datasets
Needed to make changes outside bundle upload

### Public Data
```bash
zip -j public_data.zip $ROOT/public_data/!(.gitkeep)
cp public_data.zip $DATA/training_practice/
```

### Ingestion Zip
```bash
zip -j ingestion_program.zip $ROOT/app_ingestion/ingestion_program/metadata.yaml
```

### Sample Submission Zip
```bash
zip -j sample_solution_xai.zip $ROOT/app_ingestion/program/main.py
zip -j sample_solution_xai.zip $ROOT/app_ingestion/program/pneumonia.pt
cp sample_solution_xai.zip $DATA/training_practice/
```

### Scoring Program
```bash
zip -j scoring_program.zip $ROOT/app_scoring/program/scoring.py
zip -j scoring_program.zip $ROOT/app_scoring/program/metadata.yaml
```

### Input Data
```bash
zip -j input_data.zip $ROOT/app_scoring/input/ref/!(.gitkeep)
cp input_data.zip $DATA/training_practice/
```

### Reference Data
```bash
zip -j ref_data.zip $ROOT/app_scoring/input/ref/!(.gitkeep)
cp ref_data.zip $DATA/training_practice/
```

### Starting Kit
```bash
cp $ROOT/app_ingestion/ingestion_program/metadata.yaml ./starting_kit/app_ingestion/ingestion_program/
cp $ROOT/app_ingestion/program/main.py ./starting_kit/app_ingestion/program/
cp $ROOT/app_ingestion/program/pneumonia.pt ./starting_kit/app_ingestion/program/
cp $ROOT/app_scoring/program/metadata.yaml ./stscp lin  arting_kit/app_scoring/program/
cp $ROOT/app_scoring/program/scoring.py ./starting_kit/app_scoring/program/
cp -r $ROOT/sample_docker_image ./starting_kit/
zip -r starting_kit.zip starting_kit/!(.gitkeep)
cp starting_kit.zip $DATA/training_practice/
```


## Clear data for git

### ingestion_input_data
```bash
rm -r $ROOT/app_ingestion/input_data/!(.gitkeep) # leave
```

### ingestion_prediction_output
```bash
rm -r $ROOT/app_ingestion/output/!(.gitkeep) # leave
```

### scoring_reference_data
```bash
rm -r $ROOT/app_scoring/input/ref/!(.gitkeep) # leave
```

### scoring_reference_data
```bash
rm $ROOT/starting_kit.zip
```


### scoring_results
```bash
rm -r $ROOT/app_scoring/input/res/!(.gitkeep) # leave
```

### scoring_output
```bash
rm -r $ROOT/app_scoring/output/!(.gitkeep) # leave
```

### public_data
```bash
rm -r $ROOT/public_data/!(.gitkeep) # leave
```


## Restore data

### ingestion_input_data
```bash
cp -r $DATA/dev_phase/input_data/* $ROOT/app_ingestion/input_data/
```

### scoring_reference_data
```bash
cp -r $DATA/dev_phase/reference_data/* $ROOT/app_scoring/input/ref/
```

### public_data
```bash
cp -r $DATA/public_data/* $ROOT/public_data/
```