for i in 4;
do
CUDA_VISIBLE_DEVICES=2 python main.py --type wi --num $i --max_task 500 --model mistral
done