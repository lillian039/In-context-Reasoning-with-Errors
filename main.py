from src.llm_utils.send_msg import initialize_llm, get_msg
import os
def main():
    os.makedirs('result/', exist_ok=True)
    os.makedirs('result/cache', exist_ok=True)
    initialize_llm('gpt-3.5-turbo', 'result/cache')

main()