
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

def load_gsm_data(is_socratic = False):
    file_path = '../data/grade_school_math/data/'
    if is_socratic:
        train_data = load_jsonl(file_path + 'train_socratic.jsonl')
        test_data = load_jsonl(file_path + 'test_socratic.jsonl')
    else:
        train_data = load_jsonl(file_path + 'train.jsonl')
        test_data = load_jsonl(file_path + 'test.jsonl')
    return train_data, test_data

def load_math_data(math_type):
    file_path = '../data/MATH/'
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

load_gsm_data()