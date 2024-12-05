"""
This must be use in only local
"""

import os

if __name__ == "__main__":
    # 환경 변수 삭제
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    
    print("OPENAI_API_KEY" in os.environ) #False 여야 없는것