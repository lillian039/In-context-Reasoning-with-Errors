for i in 1 3 5;
do
CUDA_VISIBLE_DEVICES=0 python main.py --type wrong_2 --num 4 --max_task 500 --model mistral --dataset math --mathtype $i --difficulty 1
done