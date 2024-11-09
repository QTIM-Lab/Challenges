# Pyenv
```bash
pyenv activate XAI
```
# Ingest
```bash
ROOT=/sddata/projects/Challenges/XAI/app_ingestion
# bash $ROOT/ingested_program/entrypoint.sh $ROOT/input_data/ $ROOT/output/ $ROOT/ingested_program/
```

# Use the inputs as arguments
```bash
input_data=$ROOT/input_data/
output=$ROOT/output/
ingested_program=$ROOT/program/
```

# Print the inputs
```bash
echo "input_data, $input_data"
echo "output, $output"
echo "ingested_program, $ingested_program"
```

# Your algorithm (example below)
```bash
python3 $ingested_program/main.py $input_data $output $ingested_program
```

# Move output for scoring
```bash
cp /sddata/projects/Challenges/XAI/app_ingestion/output/* /sddata/projects/Challenges/XAI/app_scoring/input/res/
```



# Score
```bash
ROOT=/sddata/projects/Challenges/XAI/app_scoring
```

# Use the inputs as arguments
```bash
input=$ROOT/input/
output=$ROOT/output/
program=$ROOT/program/
```

# Print the inputs
```bash
echo "input_data, $input_data"
echo "output, $output"
echo "program, $program"
```

# Your algorithm (example below)
```bash
python3 $program/scoring.py $input/ $output/
```