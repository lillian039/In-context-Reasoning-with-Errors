#!/bin/bash

model=""
remaining_args="$@"

for arg in "$@"; do
    case $arg in
        --model)
            shift 
            model=$1 
            break 
            ;;
        *)
            ;;
    esac
done


if [ "$model" == "llama" ]; then
    torchrun --nproc_per_node 1 main.py $remaining_args
else
    python main.py $remaining_args
fi