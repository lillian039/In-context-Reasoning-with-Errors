from src.llm_utils.send_msg import initialize_llm
from src.baseline import get_baseline_result
from src.utils.logger import get_logger
import os
def main():
    os.makedirs('result/', exist_ok=True)
    os.makedirs('result/cache', exist_ok=True)
    logger = get_logger('baseline')
    initialize_llm('gpt-3.5-turbo-1106', 'result/cache')
    result = get_baseline_result(4, logger)
    print(result)
main()