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
        
        # TODO: add api key
        self.client = OpenAI(
            api_key='sk-eYT6k63VWtNQo4G24a068397AfBb49258aC5Cb3f96A3C3Da',
            base_url="https://lonlie.plus7.plus/v1"
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
        chat_completion = self.client.chat.completions.create(
            messages=prompt,
            **kwargs,
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