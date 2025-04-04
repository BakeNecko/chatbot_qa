import os
from dotenv import load_dotenv

load_dotenv()  # CHECK


class Config:
    DB_PATH = os.getenv('DB_PATH', 'data/sqldb.db')
    SQL2Text_LLM = os.getenv('SQL2Text_LLM', 'deepseek-r1')
    SQLDB_DIR = os.getenv('SQLDB_DIR', 'data/sqldb.db')
    CSV_DIR = os.getenv('CSV_DIR', 'data/csv')
