from .load_data import load_gsm_data
import random
from .llm_utils.send_msg import get_msg
import re

def get_examples(train_data, k_examples):
    random.seed(0)
    examples = train_data[0:k_examples]
    str_prompt = ""

    for example in examples:
        str_prompt += "Problem: " + example['question'] + "\n"
        solution = example['answer'].split("####")[0].strip()
        str_prompt += "Solution: " + solution + "\n"
        answer = example['answer'].split("####")[1].strip()
        str_prompt += "Final Answer: " + answer + "\n\n"

    return str_prompt

def get_incontext_learning(examples, task):
    return f"""
{examples}Problem: {task}
    """

def get_result(type, k_example, logger):
    example_data, test_data = load_gsm_data(type)
    examples_prompt = get_examples(example_data, k_example)
    logger.info(examples_prompt)
    pass_task, fail_task = 0, 0
    max_try = 3
    for i, test_example in enumerate(test_data):
        content = get_incontext_learning(examples_prompt, test_example['question'])
        system = "Please give the solution of the math question and give the final answer."
        response = get_msg(content, system)
        for _ in range(max_try):
            if 'Final Answer:' not in response:
                response = get_msg(content, system)
            else:
                break
        final_answer = response.split("Final Answer:")[1].strip()
        final_answer_number = int(re.sub(r'[^0-9]', '', final_answer))
        test_answer = test_example['answer']
        correct_answer_number = int(test_answer.split("####")[1].strip())
        if final_answer_number == correct_answer_number:
            pass_task += 1
        else:
            fail_task += 1
        logger.info(f'{i}th task\n')
        logger.info(f'Final answer: LLM: {final_answer_number}, Correct: {correct_answer_number}')
        logger.info(f"\nLLM answer:\n{response}\n")
        logger.info(f'\nCorrect answer:\n{test_answer}\n')
        if i + 1 == 100:
            break
    print(pass_task, '/', pass_task + fail_task)

    return pass_task / (pass_task + fail_task)    
