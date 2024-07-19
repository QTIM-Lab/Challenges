# Code Submission Challenge Template
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
cp $ROOT/xai_code_submission_template_bundle.zip /sddata/data/Challenges/XAI/
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