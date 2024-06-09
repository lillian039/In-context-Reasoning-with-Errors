for i in {2..5};
do
CUDA_VISIBLE_DEVICES=2 python main.py --type origin --num 4 --max_task 500 --model mistral-instruct --dataset math --difficulty $i
done