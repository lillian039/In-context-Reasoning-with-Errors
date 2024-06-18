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
parser.add_argument('--dataset', type=str, default="math", help="dataset")
parser.add_argument('--mathtype', type=int, default=0, help="Only for dataset MATH")
parser.add_argument('--difficulty', type=int, default=0, help="Only for dataset MATH")

# type
# abstract_calculation : use abstract symbol to substitute the calculation process
# only_statement : only use statement in cot but ignore all the math symbols.
# pattern_only : only use patterns in cot but ignore all the statements

args = parser.parse_args()

def main():
    os.makedirs('result/', exist_ok=True)
    os.makedirs('result/cache', exist_ok=True)
    logger_name = ""
    if args.type == "origin":
        logger_name = "baseline"
    elif args.type == "wc" :
        args.type = "wrong_calculation"
    elif args.type == "wi":
        args.type = "wrong_inference"
    elif args.type == 'ns':
        args.type = "no_solution"
    elif args.type == 'swap':
         args.type = "swap"
    elif args.type == 'zs':
        args.type = "zero_shot" 
    elif args.type == "ac":
        args.type = "abstract_calculation" 
    elif args.type == "po":
        args.type = "pattern_only" 
    elif args.type == "so":
        args.type = "statement_only" 
    elif args.type == "ab":
        args.type = "abstract" 
    elif args.type == "abc":
        args.type = "abstract_abc" 


    logger = get_logger(args.type)
    for arg, value in vars(args).items():
        logger.info(f"{arg}: {value}")
        
    if args.model == "gpt" :
        model_name = 'gpt-3.5-turbo-1106'
    elif args.model == "mistral-instruct":
        model_name = 'mistral-7B-instruct'
    elif args.model == "mistral":
        model_name = 'mistral-7B-raw'
    elif args.model == "llama":
        model_name = 'llama-7B-chat'
    elif args.model == 'llama3':
        model_name = 'llama3-8B'
    initialize_llm(model_name, 'result/cache')
    result = get_result(args, logger)
    logger.info(result)
    print(result)

main()