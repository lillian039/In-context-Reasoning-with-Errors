import json
import random
import os
def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def get_sample_examples():
    file_path = ''
    train_data_so = load_jsonl(file_path + 'train_socratic.jsonl')
    random.seed(0)
    subset_indices = random.sample(range(len(train_data_so)), 16)
    train_data_so = [train_data_so[i] for i in subset_indices]
    train_data = load_jsonl(file_path + 'train.jsonl')
    train_data = [train_data[i] for i in subset_indices]
    with open('train_example.jsonl', 'w') as f:
        for example in train_data:
            f.write(json.dumps(example) + '\n')
    with open('train_example_so.jsonl', 'w') as f:
        for example in train_data_so:
            f.write(json.dumps(example) + '\n')
    
    os.makedirs('subset/', exist_ok=True)
    os.makedirs('subset/origin/', exist_ok=True)
    os.makedirs('subset_so/', exist_ok=True)
    os.makedirs('subset_so/origin', exist_ok=True)

    for i, example in enumerate(train_data):
        str_prompt = ""
        str_prompt += "Problem: " + example['question'] + "\n\n"
        solution = example['answer'].split("####")[0].strip()
        str_prompt += "Solution: " + solution + "\n\n"
        answer = example['answer'].split("####")[1].strip()
        str_prompt += "Final Answer: " + answer + "\n"
        with open(f'subset/origin/{i}.txt', 'w') as f:
            f.write(str_prompt)
    
    for i, example in enumerate(train_data_so):
        str_prompt = ""
        str_prompt += "Problem: " + example['question'] + "\n\n"
        solution = example['answer'].split("####")[0].strip()
        str_prompt += "Solution: " + solution + "\n\n"
        answer = example['answer'].split("####")[1].strip()
        str_prompt += "Final Answer: " + answer + "\n"
        with open(f'subset_so/origin/{i}.txt', 'w') as f:
            f.write(str_prompt)

get_sample_examples()