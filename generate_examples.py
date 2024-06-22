import argparse
from src.llm_utils.send_msg import initialize_llm
from src.utils.logger import get_logger
from src.load_data import load_math_data
from src.llm_utils.send_msg import get_msg
from src.utils.logger import get_logger

parser = argparse.ArgumentParser(description='llm')
parser.add_argument('--model', type=str, default="gpt", help='llm model')
args = parser.parse_args()

def main():
    logger = get_logger('answer_train_set', args)
    if args.model == "gpt" :
        model_name = 'gpt-3.5-turbo-1106'
    elif args.model == "mistral-instruct":
        model_name = 'mistral-7B-instruct'
    elif args.model == "mistral":
        model_name = 'mistral-7B-raw'
    elif args.model == "llama-instruct":
        model_name = 'llama-7B-chat'
    elif args.model == "llama":
        model_name = 'llama-7B'
    elif args.model == 'llama3':
        model_name = 'llama3-8B'

    initialize_llm(model_name, 'result/cache')

    for mathtype in 0,1,3,5:
        origin_data, _ = load_math_data('origin', mathtype, 1)
        # print(origin_data)
        logger.info(f'Math type {mathtype}')
        for j, cur_data in enumerate(origin_data):
            question = cur_data['question']
            logger.info(f'Question {j}: {question}')

            answer_train_set_prompt = f"Please give me the answer to the question:\n{question}\nAnswer:"
#             prompt2 =  f"""
# You are going to solve a math problem. 
# Problem: {question}

# Please give the solution of the math question and give the final answer in the following format, final answer should only contains the final number.

# Solution: [solution]
# Final Answer: [final answer]

# Please follow the given format to solve the problem.
#                 """   
            for i in range(2):
                logger.info(f'The {i}th answer to the question:')
                content = get_msg(answer_train_set_prompt, "")
                logger.info('\n' + content)

main()



