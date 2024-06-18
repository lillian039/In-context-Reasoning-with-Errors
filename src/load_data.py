
import json
import os
import random

class MATH_type:
    Algebra = 0
    Counting_and_Probability = 1
    Geometry = 2
    Intermediate_Algebra = 3
    Number_Theory = 4
    Pre_Algebra = 5
    Pre_Calculus = 6

def generate_gsm_jsonl(file_directory):
    data = []
    for filename in os.listdir(file_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(file_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                parts = content.split('Problem:')
                question = parts[1].split('Solution:', 1)[0]
                parts = parts[1].split('Solution:', 1)[1].split('Final Answer:', 1)
                solution = parts[0] 
                final_answer = parts[1]
                entry = {
                    'question': question.strip(),
                    'answer': solution.strip() + "\n#### " + final_answer.strip()
                }
                data.append(entry)

    with open(os.path.join(file_directory, "train_example.jsonl"), 'w', encoding='utf-8') as outfile:
        for entry in data:
            json.dump(entry, outfile)
            outfile.write('\n')

def generate_math_jsonl(file_directory, output_file, difficulty=0):
    data = []
    for filename in os.listdir(file_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(file_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                parts = content.split('Level:')
                level = parts[1].split('Problem:', 1)[0]
                if difficulty != 0:
                    diff = level.split('Level ', 1)[1][0]
                    if int(diff) != difficulty:
                        continue
                question = parts[1].split('Problem:', 1)[1].split('Solution:', 1)[0]
                parts = parts[1].split('Problem:', 1)[1].split('Solution:', 1)[1].split('Final Answer:', 1)
                solution = parts[0] 
                final_answer = parts[1]
                entry = {
                    'level': level.strip(),
                    'question': question.strip(),
                    'answer': solution.strip() + "\n#### " + final_answer.strip()
                }
                data.append(entry)
    random.seed(0)
    random.shuffle(data)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for entry in data:
            json.dump(entry, outfile)
            outfile.write('\n') 


def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def load_json_files(doc_path):
    file_names = os.listdir(doc_path)    
    file_names = sorted(file_names)
    data = []
    for file_name in file_names:
        with open(doc_path + file_name, 'r') as f:
            data.append(json.load(f))
    return data

def load_gsm_data(type, is_socratic = False):
    test_file_path = 'data/grade_school_math/data'
    if is_socratic:
        train_file_path = test_file_path + "/subset_so/" + type
        if not os.path.exists(os.path.join(train_file_path, 'train_example_socratic.jsonl')):
            generate_gsm_jsonl(train_file_path)
        example_data = load_jsonl(os.path.join(train_file_path, 'train_example_socratic.jsonl'))
        test_data = load_jsonl(os.path.join(test_file_path, 'test_socratic.jsonl'))
    else:
        train_file_path = test_file_path + "/subset/" + type
        if not os.path.exists(os.path.join(train_file_path, 'train_example.jsonl')):
            generate_gsm_jsonl(train_file_path)
        example_data = load_jsonl(os.path.join(train_file_path, 'train_example.jsonl'))
        test_data = load_jsonl(os.path.join(test_file_path, 'test.jsonl'))
    return example_data, test_data

def load_math_data(type, math_type, difficulty=0):
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
    
    example_path = file_path + f'{math_type_string}/{type}/train_example_{difficulty}.jsonl'
    test_path = file_path + f'{math_type_string}/test_{difficulty}.jsonl'
    # if not os.path.exists(example_path):
    generate_math_jsonl(file_path + f'{math_type_string}/{type}', example_path, difficulty=difficulty)
    if not os.path.exists(test_path):
        generate_math_jsonl(file_path + f'test/{math_type_string}', test_path, difficulty=difficulty)
    example_data = load_jsonl(example_path)
    test_data = load_jsonl(test_path)
    
    return example_data, test_data
