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
    CUDA_VISIBLE_DEVICES=0 torchrun --nproc_per_node 1 --master_port 12347 main.py $remaining_args
else
    python main.py $remaining_args
fi

# lsof -i:29500
# kill -9 PID 