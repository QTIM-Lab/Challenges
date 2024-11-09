# Quick run with python
```
ROOT=/sddata/projects/Challenges/XAI/app_ingestion
bash $ROOT/ingested_program/entrypoint.sh $ROOT/input_data/ $ROOT/output/ $ROOT/ingested_program/
```

# Use the inputs as arguments
```
input_data=$ROOT/input_data/
output=$ROOT/output/
ingested_program=$ROOT/program/
```

# Print the inputs
```
echo "input_data, $input_data"
echo "output, $output"
echo "ingested_program, $ingested_program"
```

# Your algorithm (example below)
```
cd $ingested_program
python3 $ingested_program/main.py $input_data $output $ingested_program
```