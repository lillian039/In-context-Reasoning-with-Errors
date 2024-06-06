from .load_data import load_gsm_data
import random
from .llm_utils.send_msg import get_msg
import re

def get_examples(train_data, k_examples, if_solution=True):
    random.seed(0)
    examples = train_data[0:k_examples]
    str_prompt = ""

    for example in examples:
        str_prompt += "Problem: " + example['question'] + "\n"
        solution = example['answer'].split("####")[0].strip()
        if if_solution:
            str_prompt += "Solution: " + solution + "\n"
        answer = example['answer'].split("####")[1].strip()
        str_prompt += "Final Answer: " + answer + "\n\n"

    return str_prompt

def get_examples_swap(train_data, k_examples):
    examples = train_data[0:k_examples]
    str_prompt = ""

    for example in examples:
        str_prompt += "Problem: " + example['question'] + "\n"
        solution = example['answer'].split("####")[0].strip()
        answer = example['answer'].split("####")[1].strip()

        str_prompt += "Final Answer: " + answer + "\n"
        str_prompt += "Solution: " + solution + "\n\n"
       
    return str_prompt

def get_incontext_learning(examples, task):
    return f"""
{examples}Problem: {task}
    """

def get_zero_shot_learning(task):
    return f"""
Problem: {task}

Please give the solution of the math question and give the final answer in the following format, final answer should only contains the final number.
Solution: [solution]
Final Answer: [final answer]
    """

def get_result(type, k_example, logger, max_task):
    example_data, test_data = load_gsm_data(type)
    if_solution = type != "no_solution"
    if type == 'swap':
        examples_prompt = get_examples_swap(example_data, k_example)
    else:
        examples_prompt = get_examples(example_data, k_example, if_solution)
    # logger.info(examples_prompt)
    pass_task, fail_task = 0, 0
    max_try = 5
    for i, test_example in enumerate(test_data):
        if type == 'zero_shot':
            content = get_zero_shot_learning(test_example['question'])
        else:
            content = get_incontext_learning(examples_prompt, test_example['question'])
        if if_solution:
            system = "Please give the solution of the math question and give the final answer."
        else:
            system = "Please give the final answer of the math question."
        response = get_msg(content, system)
        for _ in range(max_try):
            logger.info(response)
            if 'Final Answer:' not in response:
                response = get_msg(content, system)
            else:
                break
        try:
            final_answer = response.split("Final Answer:")[1].strip()
            match = re.search(r'\d', final_answer)
            final_answer = final_answer[match.start():]
            final_answer = final_answer.split(' ')[0]
            final_answer_number = int(re.sub(r'[^0-9]', '', final_answer))
        except:
            print(final_answer)
            final_answer_number = -1

        test_answer = test_example['answer']
        test_answer_number = test_answer.split("####")[1].strip()
        test_answer_number = re.sub(r'[^0-9]', '', test_answer_number)
        correct_answer_number = int(test_answer_number)
        if final_answer_number == correct_answer_number:
            pass_task += 1
        else:
            fail_task += 1
        logger.info(f'{i}th task\n')
        logger.info(f'Final answer: LLM: {final_answer_number}, Correct: {correct_answer_number}')
        logger.info(f"\nLLM answer:\n{response}\n")
        logger.info(f'\nCorrect answer:\n{test_answer}\n')
        if i + 1 == max_task:
            break
    print(pass_task, '/', pass_task + fail_task)

    return pass_task / (pass_task + fail_task)    
