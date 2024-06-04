from src.llm_utils.send_msg import initialize_llm
from src.baseline import get_result
from src.utils.logger import get_logger
import os
import argparse

parser = argparse.ArgumentParser(description='llm')

parser.add_argument('--model', type=str, default="gpt", help='llm model')
parser.add_argument('--type', type=str, default="origin", help='example type')
parser.add_argument('--num', type=int, default=4, help='example number')

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
    logger = get_logger(logger_name)
    for arg, value in vars(args).items():
        logger.info(f"{arg}: {value}")
    if args.model == "gpt" :
        initialize_llm('gpt-3.5-turbo-1106', 'result/cache')
        result = get_result(args.type, args.num, logger)
        print(result)

main()