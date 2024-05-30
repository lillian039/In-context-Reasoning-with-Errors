from .cache_system import get_llm, insert_request

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
    return completion.choices[0].message.content