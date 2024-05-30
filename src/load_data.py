
import json
def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def load_gsm_data():
    file_path = '../data/grade_school_math/data/'
    train_data = load_jsonl(file_path + 'train.jsonl')
    test_data = load_jsonl(file_path + 'test.jsonl')
    train_socratic_data = load_jsonl(file_path + 'train_socratic.jsonl')
    test_socratic_data = load_jsonl(file_path + 'test_socratic.jsonl')
    return train_data, test_data, train_socratic_data, test_socratic_data