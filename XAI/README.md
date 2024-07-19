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
cp /sddata/projects/Challenges/XAI/xai_code_submission_template_bundle.zip /sddata/data/Challenges/XAI/
```

## Clear data for git



### input_data
```bash
/sddata/projects/Challenges/XAI/app_ingestion/input_data
```

### prediction_output
```bash
/sddata/projects/Challenges/XAI/app_ingestion/output
```

### reference_data
```bash
/sddata/projects/Challenges/XAI/app_ingestion/output
```

### results
```bash

```

### scoring_output
```bash

```