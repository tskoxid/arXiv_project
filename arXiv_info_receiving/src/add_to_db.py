from arXiv_info_receiving.src.arXiv_info import get_info_arxiv
import pandas as pd
import time
import logging


def to_db(arxiv_df: pd.DataFrame, set_id: set, url_article: str):
    if 'arxiv.org' in url_article:
        id_url = url_article.split('/')[-1]
        if 'v' in id_url:
            id_url = id_url[:-2]
        if id_url not in set_id:
            arxiv_data = get_info_arxiv(id_url)
            arxiv_df = arxiv_df.append(pd.DataFrame(arxiv_data, index=[0]), ignore_index=True)
            set_id.add(id_url)
            time.sleep(3)
            return arxiv_df, set_id
        else:
            logging.warning("This article already in database")
            return arxiv_df, set_id
    else:
        logging.warning("This url not from arXiv")
        return arxiv_df, set_id
