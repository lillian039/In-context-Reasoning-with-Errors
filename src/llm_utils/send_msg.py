from .cache_system import get_llm, insert_request
from transformers import AutoModelForCausalLM, AutoTokenizer

client = None
def initialize_llm(llm_model, llm_cache_path):
    global client
    client = get_llm(llm_model, llm_cache_path)


def get_msg(content, role_information):
    prompt = [
        {"role": "system", "content": role_information},
        {"role": "user", "content": content}
    ]

    ith = insert_request(prompt)
    completion = client.request(prompt, ith)
    if completion is None:
        print('No completion generated')
        return None
    if 'gpt3.5' in client.model:
        return completion.choices[0].message.content
    elif 'gpt2' in client.model:
        return completion
    elif 'mistral' in client.model:
        return completion
    elif client.model == 'llama-7B-chat':
        print(completion[0])
        return completion[0]['generation']['content']
    elif client.model == 'llama-7B':
        return completion[0]['generation']
    elif client.model == 'llama3-8B':
        return completion[0]['generation']
        
