
CUDA_VISIBLE_DEVICES=1 torchrun --nproc_per_node 1 --master_port 12347 main.py  --model llama3

# lsof -i:29500
# kill -9 PID 