import os
import pandas as pd

import pandas as pd
from sqlalchemy import create_engine, inspect

from src.config import Config


class PrepareSQLFromTabularData:
    """
    Класс, который подготавливает базу данных SQL из файлов CSV в указанном каталоге.

    Этот класс считывает каждый файл, преобразует данные в DataFrame, 
    а затем сохраняет их в виде таблицы в базе данных SQLite, 
    которая задается конфигурацией приложения.   
    """

    def __init__(self, files_dir) -> None:
        cfg = Config
        self.files_directory = files_dir
        self.file_dir_list = os.listdir(files_dir)
        db_path = f"sqlite:///{cfg.DB_PATH}"
        self.engine = create_engine(db_path)
        print("Number of csv files:", len(self.file_dir_list))

    def _prepare_db(self):
        for file in self.file_dir_list:
            full_file_path = os.path.join(self.files_directory, file)
            file_name, file_extension = os.path.splitext(file)
            if file_extension == ".csv":
                df = pd.read_csv(full_file_path)
            else:
                raise ValueError("The selected file type is not supported")
            df.to_sql(file_name, self.engine, index=False)

    def _validate_db(self):
        insp = inspect(self.engine)
        table_names = insp.get_table_names()
        print("==============================")
        print("Available table nasmes in created SQL DB:", table_names)
        print("==============================")

    def run_pipeline(self):
        self._prepare_db()
        self._validate_db()
