for i in 0;
do
CUDA_VISIBLE_DEVICES=2 python main.py --type llama2 --num 4 --max_task 500 --model mistral --dataset math --mathtype $i --difficulty 1
done