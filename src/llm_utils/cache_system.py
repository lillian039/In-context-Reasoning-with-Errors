import os
import numpy as np
import hashlib
import dill
import copy
from openai import OpenAI, AzureOpenAI
import time

def get_llm(llm_model, llm_cache_path, llm_temperature=1.0, llm_seed=0):
    default_kwargs = {
        'model': llm_model,
        'temperature': llm_temperature,
    }
    return LLM(
        cache_path=llm_cache_path,
        seed=llm_seed,
        default_kwargs=default_kwargs,
    )

prompt_set_number = {}

def insert_request(prompt):
    harsh_prompt = hashlib.md5((str(sorted(prompt, key=str))).encode('utf-8')).hexdigest()
    ith = 0
    if harsh_prompt in prompt_set_number:
        prompt_set_number[harsh_prompt] += 1
        ith = prompt_set_number[harsh_prompt]
    else:
        ith = 1
        prompt_set_number[harsh_prompt] = 1
    return ith

class LLM:
    def __init__(self, cache_path=None, seed=0, default_kwargs=None,):
        if cache_path is None:
            curdir = os.path.dirname(os.path.abspath(__file__))
            cache_path = os.path.join(curdir, 'cache')
        self.cache_path = cache_path
        os.makedirs(self.cache_path, exist_ok=True)
        self.caches = {}
        self.seed = seed
        self.default_kwargs = default_kwargs if default_kwargs is not None else dict()
        self.model = self.default_kwargs['model']
        print(self.default_kwargs['model'])
        if 'mistral' in self.default_kwargs['model']:
            from mistral_inference.model import Transformer
            from mistral_inference.generate import generate

            from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
            from mistral_common.protocol.instruct.messages import UserMessage
            from mistral_common.protocol.instruct.request import ChatCompletionRequest

        # TODO: add api key
        if 'gpt' in self.default_kwargs['model']:
            self.client = OpenAI(
                api_key='sk-eYT6k63VWtNQo4G24a068397AfBb49258aC5Cb3f96A3C3Da',
                base_url="https://lonlie.plus7.plus/v1"
            )
        elif self.default_kwargs['model'] == 'mistral-7B-instruct':
            self.client = Transformer.from_folder("/userhome/hukeya/mistral_models/7B_instruct")  # change to extracted model dir
            self.tokenizer = MistralTokenizer.from_file("/userhome/hukeya/mistral_models/7B_instruct/tokenizer.model.v3")  # change to extracted tokenizer file
        elif self.default_kwargs['model'] == 'mistral-7B-raw':
            self.client = Transformer.from_folder("/userhome/hukeya/mistral_models/7B")  # change to extracted model dir
            self.tokenizer = MistralTokenizer.from_file("/userhome/hukeya/mistral_models/7B/tokenizer.model.v3")  # change to extracted tokenizer file
        elif 'llama-7B' in self.default_kwargs['model']:
            from llama import Llama

            self.generator = Llama.build(
                ckpt_dir="../llama/llama-2-7b/",
                tokenizer_path="../llama/tokenizer.model",
                max_seq_len=2048,
                max_batch_size=4,
            )

    def request(self, prompt, nth, kwargs=None):
        if kwargs is None:
            kwargs = copy.deepcopy(self.default_kwargs)
        else: 
            kwargs = copy.deepcopy(kwargs)
            for k in self.default_kwargs:
                if k not in kwargs:
                    kwargs[k] = self.default_kwargs[k]
        request_id = hashlib.md5(str((
            tuple(sorted(prompt, key=str)),
            tuple(sorted(kwargs.items(), key=str)),
        )).encode('utf-8')).hexdigest()

        # Handle cache
        if request_id in self.caches and self.seed in self.caches[request_id]['index'] and nth < len(self.caches[request_id]['index'][self.seed]):
            cache = self.caches[request_id]
        elif os.path.exists(os.path.join(self.cache_path, request_id+'.dill')):
            with open(os.path.join(self.cache_path, request_id+'.dill'), 'rb') as f:
                cache = dill.load(f)
        else:
            cache = {'responds': [], 'index': {}}
        if self.seed in cache['index']:
            index = cache['index'][self.seed]
            if len(index) < len(cache['responds']):
                np_rng = np.random.default_rng(self.seed)
                index = index + list(np_rng.permutation(list(range(len(index), len(cache['responds'])))))
        elif len(cache['responds']):
            np_rng = np.random.default_rng(self.seed)
            index = list(np_rng.permutation(len(cache['responds'])))
        else:
            index = []

        # Request
        if nth > len(index):
            print("new")
            assert nth == len(index) + 1, f'{nth} {len(index)}'
            response = self.new_request(prompt, kwargs,)
            cache['responds'].append(response)
            index.append(len(cache['responds']) - 1)
            cache['index'][self.seed] = index
        response = cache['responds'][index[nth - 1]]

        # Save cache
        self.caches[request_id] = cache
        with open(os.path.join(self.cache_path, request_id+'.dill'), 'wb') as f:
            dill.dump(cache, f)

        return response
    
    def insert_request(self, prompt, completion, nth):
        kwargs = copy.deepcopy(self.default_kwargs)
        request_id = hashlib.md5(str((
            tuple(sorted(prompt, key=str)),
            tuple(sorted(kwargs.items(), key=str)),
        )).encode('utf-8')).hexdigest()
        if request_id in self.caches and self.seed in self.caches[request_id]['index'] and nth < len(self.caches[request_id]['index'][self.seed]):
            cache = self.caches[request_id]
        elif os.path.exists(os.path.join(self.cache_path, request_id+'.dill')):
            with open(os.path.join(self.cache_path, request_id+'.dill'), 'rb') as f:
                cache = dill.load(f)
        else:
            cache = {'responds': [], 'index': {}}
        
        if self.seed in cache['index']:
            index = cache['index'][self.seed]
            if len(index) < len(cache['responds']):
                np_rng = np.random.default_rng(self.seed)
                index = index + list(np_rng.permutation(list(range(len(index), len(cache['responds'])))))
        elif len(cache['responds']):
            np_rng = np.random.default_rng(self.seed)
            index = list(np_rng.permutation(len(cache['responds'])))
        else:
            index = []

        if nth > len(index):
            assert nth == len(index) + 1, f'{nth} {len(index)}'
            response = completion
            if response is None:
                return None
            cache['responds'].append(response)
            index.append(len(cache['responds']) - 1)
            cache['index'][self.seed] = index
        response = cache['responds'][index[nth - 1]]

        # Save cache
        self.caches[request_id] = cache
        with open(os.path.join(self.cache_path, request_id+'.dill'), 'wb') as f:
            dill.dump(cache, f)

        return response


    def _new_request(self, prompt, kwargs):
        if 'gpt' in kwargs['model']:
            chat_completion = self.client.chat.completions.create(
                messages=prompt,
                **kwargs,
            )
        elif 'mistral' in kwargs['model']:
            from mistral_inference.model import Transformer
            from mistral_inference.generate import generate

            from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
            from mistral_common.protocol.instruct.messages import UserMessage
            from mistral_common.protocol.instruct.request import ChatCompletionRequest
            completion_request = ChatCompletionRequest(messages=[UserMessage(content=prompt[1]['content'])])

            tokens = self.tokenizer.encode_chat_completion(completion_request).tokens

            out_tokens, _ = generate([tokens], self.client, max_tokens=512, temperature=1.0, eos_id=self.tokenizer.instruct_tokenizer.tokenizer.eos_id)
            chat_completion = self.tokenizer.instruct_tokenizer.tokenizer.decode(out_tokens[0])
        elif 'llama-7B' in kwargs['model']:
            from llama import Dialog
            from typing import List
            system_content = "You are a helpful assistant. You only need to answer the last question. There are solutions to some math questions for reference. Please follow the format of the examples."
            # prompt = [
            #     {"role": "system", "content": "You are a helpful assistant. You only need to answer the last question. There are solutions to some math questions for reference. Please follow the format of the examples."},
            #     {"role": "user", "content": prompt[1]['content']}
            # ]
            prompt = system_content + "\n" + prompt[1]['content']
            prompts : List[str] = [prompt,]
            chat_completion = self.generator.text_completion(
                    prompts,
                    max_gen_len=512,
                    temperature=0.6,
                    top_p=0.9,
                )
        return chat_completion
    
    def new_request(self, prompt, kwargs):
        # TODO: Handle rate limit & retry
        try:
            response = self._new_request(prompt, kwargs)
        except Exception as e:
            time.sleep(30)
            print(e)
            try:
                response = self._new_request(prompt, kwargs)
            except Exception as e:
                print(e)
                time.sleep(30)
                try:
                    response = self._new_request(prompt, kwargs)
                except Exception as e:
                    print(e)
                    response = None    
                    time.sleep(30)
        return response
