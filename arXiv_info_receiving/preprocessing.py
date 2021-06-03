import pandas as pd


def split(change_id: str):
    split_id = change_id.split('.')[0]
    if len(split_id) == 3:
        return '0' + change_id
    else:
        return change_id


def preprocessing_dataset(df: pd.DataFrame):
    df['id'] = df['id'].apply(lambda x: split(str(x)))
    return df
