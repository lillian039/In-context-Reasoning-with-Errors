from datasets import load_dataset,list_datasets

def load_gsm8k_dataset():
    print(list_datasets())
    dataset = load_dataset('gsm8k')
    return dataset

load_gsm8k_dataset()
