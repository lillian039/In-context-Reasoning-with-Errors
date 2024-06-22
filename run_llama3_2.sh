
# CUDA_VISIBLE_DEVICES=1 torchrun --nproc_per_node 1 --master_port 12345 main.py  --model llama3 --dataset gsm
for i in 5;
do
CUDA_VISIBLE_DEVICES=3 torchrun --nproc_per_node 1 --master_port 12348 main.py --model llama3  --type origin --dataset math --mathtype $i --difficulty 1
done
# lsof -i:29500
# kill -9 PID 