from src.llm_utils.send_msg import initialize_llm, get_msg
from src.baseline import get_baseline_result
import os
def main():
    os.makedirs('result/', exist_ok=True)
    os.makedirs('result/cache', exist_ok=True)
    initialize_llm('gpt3.5', 'result/cache')
    result = get_baseline_result()
    print(result)
main()