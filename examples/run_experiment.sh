#!/bin/bash

export WANDB_API_KEY=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

model_names=("dkt" "sakt" "akt" "simplekt" "dtransformer")
dataset_names=("llama3.2:latest" "mistral" "qwen3.5:latest" "qwen2.5:latest" "deepseek-r1:latest")


for model_name in "${model_names[@]}"; do
    for dataset_name in "${dataset_names[@]}"; do
        
        if [[ $dataset_name != "assist2009" ]]; then
            dataset_name="smart_tutor_$dataset_name"
        fi

        EXPERIMENT_PATH="./experiment_models/${dataset_name}_${model_name}*"
        FILE=$(find -type d -path "$EXPERIMENT_PATH" -print -quit)
        
        if [[ -z "$FILE" ]]; then
            echo "Running $model_name on $dataset_name"
            python "wandb_"$model_name"_train.py" --dataset_name=$dataset_name --save_dir="experiment_models" --use_wandb=0
        else
            echo "$model_name ($dataset_name) already exists, skipping training"
            continue
        fi

        FILE=$(find -type d -path "$EXPERIMENT_PATH" -print -quit)
        echo $FILE

        if [[ -z "$FILE" ]]; then
            echo "No file found with substring '$EXPERIMENT_PATH'" >&2
            exit 1
        fi

        if [[ $(find -type d -path "$EXPERIMENT_PATH" | wc -l) -ne 1 ]]; then
            echo "Multiple directories found with substring '$EXPERIMENT_PATH'" >&2
            echo "Number of directories found: " $(find -type d -path "$EXPERIMENT_PATH" | wc -l)
            exit 1
        fi

        python "wandb_predict.py" --save_dir=$FILE --use_wandb=0 --bz=64
    done
done