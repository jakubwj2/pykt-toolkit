#!/bin/bash

DIR="${1:-.}"

dataset_name=$2

shopt -s nullglob

for file in "$DIR"/wandb_*_train.py; do
  if [[ "$(basename "$file")" != "wandb_train.py" ]]; then
    echo "Running $file"
    python "$file" --dataset_name=$dataset_name --use_wandb=0 --add_uuid=0
  fi
done