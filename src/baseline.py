from .load_data import load_gsm_data
import random
from .llm_utils.send_msg import get_msg

def get_examples(train_data, k_examples):
    examples = []
    for i in range(k_examples):
        example = random.choice(train_data)
        examples.append(example)
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
def get_baseline_result():
    train_data, test_data = load_gsm_data()
    examples_prompt = get_examples(train_data, 5)
    test_example = random.choice(test_data)['question']
    content = get_incontext_learning(examples_prompt, test_example)
    system = "Please give the solution of the math question and give the final answer."
    print(content)
    response = get_msg(content, system)
    return response    
