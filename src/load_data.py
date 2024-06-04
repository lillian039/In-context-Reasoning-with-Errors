
import json
import os

class MATH_type:
    Algebra = 0
    Counting_and_Probability = 1
    Geometry = 2
    Intermediate_Algebra = 3
    Number_Theory = 4
    Pre_Algebra = 5
    Pre_Calculus = 6

def generate_jsonl(file_directory):
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
        example_data = load_jsonl(os.path.join(train_file_path, 'train_example_socratic.jsonl'))
        test_data = load_jsonl(os.path.join(test_file_path, 'test_socratic.jsonl'))
    else:
        train_file_path = test_file_path + "/subset/" + type
        example_data = load_jsonl(os.path.join(train_file_path, 'train_example.jsonl'))
        test_data = load_jsonl(os.path.join(test_file_path, 'test.jsonl'))
    return example_data, test_data

def load_math_data(math_type):
    file_path = 'data/MATH/'
    if math_type == MATH_type.Algebra:
        train_data = load_json_files(file_path + 'train/algebra/')
        test_data = load_json_files(file_path + 'test/algebra/')
    elif math_type == MATH_type.Counting_and_Probability:
        train_data = load_json_files(file_path + 'train/counting_and_probability/')
        test_data = load_json_files(file_path + 'test/counting_and_probability/')
    elif math_type == MATH_type.Geometry:
        train_data = load_json_files(file_path + 'train/geometry/')
        test_data = load_json_files(file_path + 'test/geometry/')
    elif math_type == MATH_type.Intermediate_Algebra:
        train_data = load_json_files(file_path + 'train/intermediate_algebra/')
        test_data = load_json_files(file_path + 'test/intermediate_algebra/')
    elif math_type == MATH_type.Number_Theory:
        train_data = load_json_files(file_path + 'train/number_theory/')
        test_data = load_json_files(file_path + 'test/number_theory/')
    elif math_type == MATH_type.Pre_Algebra:
        train_data = load_json_files(file_path + 'train/pre_algebra/')
        test_data = load_json_files(file_path + 'test/pre_algebra/')
    elif math_type == MATH_type.Pre_Calculus:
        train_data = load_json_files(file_path + 'train/pre_calculus/')
        test_data = load_json_files(file_path + 'test/pre_calculus/')
    else:
        raise ValueError('Invalid math type')   
    
    return train_data, test_data

# load_gsm_data()