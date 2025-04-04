from src.config import Config
from src.utils.prepare_csv_to_sqlite import PrepareSQLFromTabularData


if __name__ == "__main__":
    prep_sql_instance = PrepareSQLFromTabularData(Config.CSV_DIR)
    prep_sql_instance.run_pipeline()
