import pandas as pd
from arXiv_info_receiving.src.preprocessing import preprocessing_dataset


def download_data(path_to_file: str):
    database = pd.read_json(path_to_file, lines=True)
    database = preprocessing_dataset(database)
    database_ids = set(database['id'])
    return database, database_ids
