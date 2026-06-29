import os                    # стандартная библиотека Python
from dotenv import load_dotenv  # импорт из python-dotenv

load_dotenv()  # читает .env файл и загружает переменные

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # достаёт значение переменной
BASE_URL = os.getenv('BASE_URL')          # достаёт значение переменной