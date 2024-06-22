import argparse
from src.llm_utils.send_msg import initialize_llm
from src.utils.logger import get_logger
from src.load_data import load_math_data, MATH_type
from src.llm_utils.send_msg import get_msg
from src.utils.logger import get_logger
import os


def remove_leading_spaces(text):
    lines = text.split('\n')
    stripped_lines = [line.lstrip() for line in lines]
    stripped_text = '\n'+''.join(stripped_lines)
    return stripped_text


def get_file_path(math_type):
    file_path = 'data/MATH/'
    math_type_string = ""
    if math_type == MATH_type.Algebra:
        math_type_string = 'algebra'
    elif math_type == MATH_type.Counting_and_Probability:
        math_type_string = 'counting_and_probability'
    elif math_type == MATH_type.Geometry:
        math_type_string = 'geometry'
    elif math_type == MATH_type.Intermediate_Algebra:
        math_type_string = 'intermediate_algebra'
    elif math_type == MATH_type.Number_Theory:
        math_type_string = 'number_theory'
    elif math_type == MATH_type.Pre_Algebra:
        math_type_string = 'prealgebra'
    elif math_type == MATH_type.Pre_Calculus:
        math_type_string = 'precalculus'
    else:
        raise ValueError('Invalid math type')   
    file_path += math_type_string + '/'
    return file_path

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

            # answer_train_set_prompt = f"Please give me the answer to the question:\n{question}\nAnswer:"
            prompt2 =  f"""
This is only a format. You should answer the questions according to their statement.
Problem: [Problem statement]
Solution: [The method step by step to solve the problem]
Final Answer: [Directly give the answer without any statement]

Problem: {question}
                """ 
            for i in range(32):
                logger.info(f'The {i}th answer to the question:')
                content = get_msg(prompt2, "")
                try:
                    if "Final Answer:" and "Solution:" in content:
                        final_answer_tip = "Final Answer:"
                        solution_tip =  "Solution:"
                    elif "Final Answer:" and "The final answer is" in content:
                        final_answer_tip = "The final answer is"
                        solution_tip =  "Solution:"
                    else:
                        continue
                    solution = content.split(solution_tip)[1]
                    solution = solution.split(final_answer_tip)[0]
                    answer = content.split(final_answer_tip)[1]
                    answer = answer.split('\n')[0]
                    if '.' == answer[-1]:
                        answer = answer[:-1]
                    solution = remove_leading_spaces(solution)
                    solution = solution.strip()
                    answer = answer.strip()
                    if "=" in answer:
                        answer = answer.split('=')[1]
                        if "$" in answer:
                            answer = "$" + answer
                    if solution == "" and answer == "":
                        continue
                    logger.info(f"Solution:\n{solution}")
                    logger.info(f"Answer: {answer}")
                    file_path = get_file_path(mathtype)
                    file_path = file_path + f'{model_name}/'
                    os.makedirs(file_path, exist_ok=True)
                    with open(file_path + f'{j}.txt', 'w') as f:
                        write_content = f"Level: Level 1\nProblem: {question}\n\nSolution: {solution}\n\nFinal Answer: {answer}"
                        f.write(write_content)
                    break
                
                except Exception as e:
                    # print(e)
                    # exit(0)
                    pass
                # print(content)
                # logger.info('\n' + content)
            # exit(0)

main()



