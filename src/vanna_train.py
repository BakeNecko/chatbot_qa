import json
from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore

from src.config import Config

tablle_ddl = """
CREATE TABLE IF NOT EXISTS freelancer_earnings (
    id INTEGER PRIMARY KEY,
    freelancer_id BIGINT,
    job_category TEXT CHECK (job_category IN ('Web Development', 'App Development', 'Data Entry', 'Digital Marketing', 'Customer Support', 'Content Writing', 'Graphic Design', 'SEO')),
    platform TEXT CHECK (platform IN ('Toptal', 'Fiverr', 'PeoplePerHour', 'Upwork', 'Freelancer')),
    experience_level TEXT CHECK (experience_level IN ('Beginner', 'Intermediate', 'Expert')),
    client_region TEXT CHECK (client_region IN ('Asia', 'Australia', 'UK', 'Europe', 'USA', 'Middle East', 'Canada')),
    payment_method TEXT CHECK (payment_method IN ('Mobile Banking', 'PayPal', 'Bank Transfer', 'Crypto')),
    job_completed BIGINT,
    earnings_usd BIGINT,
    hourly_rate REAL,
    job_success_rate REAL,
    client_rating REAL,
    job_duration_days BIGINT,
    project_type TEXT CHECK (project_type IN ('Fixed', 'Hourly')),
    rehire_rate REAL,
    marketing_spend BIGINT
);
"""


def get_vanna():
    class MyVanna(ChromaDB_VectorStore, Ollama):
        def __init__(self, config=None):
            ChromaDB_VectorStore.__init__(self, config=config)
            Ollama.__init__(self, config=config)

    vn = MyVanna(config={'model': Config.SQL2Text_LLM,
                 'path': 'data/chromadb'})
    vn.connect_to_sqlite(Config.DB_PATH)
    vn.remove_training_data('1-sql')
    df_ddl = vn.run_sql(
        "SELECT type, sql FROM sqlite_master WHERE sql is not null")
    for ddl in df_ddl['sql'].to_list():
        vn.train(ddl=ddl)
    vn.train(ddl=tablle_ddl)
    with open('q.json', 'r', encoding='utf-8') as file:
        test_pars = json.load(file)
        for par in test_pars:
            vn.train(question=par['question'], sql=par['sql'])
    return vn
