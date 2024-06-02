# In-context-Reasoning-with-Errors


Set up environment for mistral-7B
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
