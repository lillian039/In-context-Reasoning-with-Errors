import json
import random
import os

from util import load_jsonl

class MATH_type:
    Algebra = 0
    Counting_and_Probability = 1
    Geometry = 2
    Intermediate_Algebra = 3
    Number_Theory = 4
    Pre_Algebra = 5
    Pre_Calculus = 6

def get_string(math_type):
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
    
    return math_type_string
 

def generate_math_jsonl(file_directory, output_file, difficulty=0):
    from util import remove_boxed, last_boxed_only_string
    data = []
    for filename in os.listdir(file_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(file_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
                if difficulty==0 or content.get("level") == f"Level {difficulty}": 
                    solution = content.get('solution', '').strip()
                    entry = {
                        'level': content.get('level'),
                        'question': content.get('problem', '').strip(),
                        'answer': solution + "\n#### " + remove_boxed(last_boxed_only_string(solution))
                    }
                    data.append(entry)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for entry in data:
            json.dump(entry, outfile)
            outfile.write('\n') 


def load_math_data(math_type, difficulty=0):
    file_path = ''
    math_type_string = get_string(math_type)

    example_path = file_path + f'{math_type_string}/train_{difficulty}.jsonl'
    test_path = file_path + f'{math_type_string}/test_{difficulty}.jsonl'
    if not os.path.exists(example_path):
        generate_math_jsonl(file_path + f'train/{math_type_string}', example_path, difficulty=difficulty)
    if not os.path.exists(test_path):
        generate_math_jsonl(file_path + f'test/{math_type_string}', test_path, difficulty=difficulty)
    example_data = load_jsonl(example_path)
    test_data = load_jsonl(test_path)
    
    return example_data, test_data


def get_sample_examples(math_type):    
    math_type_string = get_string(math_type)
    file_dir = math_type_string + '/'

    train_data_final = []
    for difficulty in range(1, 6):
        file_path = file_dir + f'train_{difficulty}.jsonl'
        train_data = load_jsonl(file_path)
        random.seed(0) 
        subset_indices = random.sample(range(len(train_data)), 4)
        for i in subset_indices:
            train_data_final.append(train_data[i])

    random.shuffle(train_data_final)

    if not os.path.exists(file_dir + 'origin'):
        os.mkdir(file_dir + 'origin')

    with open(file_dir + "origin/train_example_0.jsonl",'w') as f:
        for example in train_data_final:
            f.write(json.dumps(example) + '\n')

    for i, example in enumerate(train_data_final):
        str_prompt = ""
        str_prompt += "Level: " + example['level'] + "\n\n"
        str_prompt += "Problem: " + example['question'] + "\n\n"
        solution = example['answer'].split("####")[0].strip()
        str_prompt += "Solution: " + solution + "\n\n"
        answer = example['answer'].split("####")[1].strip()
        str_prompt += "Final Answer: " + answer + "\n"
        with open(file_dir + f'origin/{i}.txt', 'w') as f:
            f.write(str_prompt)
    
