from src.llm_utils.send_msg import initialize_llm
from src.pipeline import get_result
from src.utils.logger import get_logger
import os
import argparse

parser = argparse.ArgumentParser(description='llm')

parser.add_argument('--model', type=str, default="gpt", help='llm model')
parser.add_argument('--type', type=str, default="origin", help='example type')
parser.add_argument('--num', type=int, default=4, help='example numbers')
parser.add_argument('--max_task', type=int, default=500, help='Q&A numbers')

args = parser.parse_args()

def main():
    os.makedirs('result/', exist_ok=True)
    os.makedirs('result/cache', exist_ok=True)
    logger_name = ""
    if args.type == "origin":
        logger_name = "baseline"
    elif args.type == "wc" :
        args.type = "wrong_calculate"
        logger_name = "wrong_calculate"
    elif args.type == "wi":
        args.type = "wrong_inference"
        logger_name = "wrong_inference"
    elif args.type == 'ns':
        args.type = "no_solution"
        logger_name = "no_solution"
    elif args.type == 'swap':
        logger_name = "swap"
    elif args.type == 'zs':
        logger_name = "zero_shot"
        args.type = "zero_shot" 

    logger = get_logger(logger_name)
    for arg, value in vars(args).items():
        logger.info(f"{arg}: {value}")
        
    if args.model == "gpt" :
        model_name = 'gpt-3.5-turbo-1106'
    elif args.model == "mistral-instruct":
        model_name = 'mistral-7B-instruct'
    elif args.model == "mistral":
        model_name = 'mistral-7B-raw'
    elif args.model == "llama":
        model_name = 'llama-7B'
    initialize_llm(model_name, 'result/cache')
    result = get_result(args.type, args.num, logger, args.max_task)
    logger.info(result)
    print(result)

main()