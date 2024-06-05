from src.llm_utils.send_msg import initialize_llm
from src.baseline import get_result
from src.utils.logger import get_logger
import os
import argparse

parser = argparse.ArgumentParser(description='llm')

parser.add_argument('--model', type=str, default="gpt", help='llm model')
parser.add_argument('--type', type=str, default="origin", help='example type')
parser.add_argument('--num', type=int, default=4, help='example number')
parser.add_argument('--max_task', type=int, default=200, help='example number')

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
    elif args.type == 'ns':
        args.type = "no_solution"
        logger_name = "no_solution"
    elif args.type == 'swap':
        logger_name = "swap"
    logger = get_logger(logger_name)
    for arg, value in vars(args).items():
        logger.info(f"{arg}: {value}")
    if args.model == "gpt" :
        model_name = 'gpt-3.5-turbo-1106'
    elif args.model == "mistral":
        model_name = 'mistral-7B'
    initialize_llm(model_name, 'result/cache')
    result = get_result(args.type, args.num, logger, args.max_task)
    print(result)

main()