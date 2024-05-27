import os
from dotenv import load_dotenv
dotenv_path = '.env'
load_dotenv(dotenv_path)
# DB 경로를 .env에서 가져와서 상수로 고정
database_path = os.getenv('DATABASE_PATH')