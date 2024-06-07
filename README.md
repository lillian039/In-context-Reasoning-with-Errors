# In-context-Reasoning-with-Errors


### Set up environment for mistral-7B
```
https://github.com/mistralai/mistral-inference/blob/main/README.md
```

- Build a new conda environment 

  ```
  conda create -n llm  python=3.11
  conda activate llm
  pip install xformers -i  http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
  pip install mistral-inference -i  http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
  ```

- Follow the instructions in the github repo's README file

### Dataset

For MATH dataset, we randomly select 4 examples for each level and each subproblem.

The method we generate the examples can be found in `generate.py`. Once randomly generated, we can find the original examples in `/origin/train_example_0.jsonl`, where "0" means all the levels are included. You can also point out the specific level.

### Run
```
bash run.sh --model [gpt/mistral/llama/] --type [origin/wc/wi/...] --num [4/8/...] --max_task [500/1000/...]
```