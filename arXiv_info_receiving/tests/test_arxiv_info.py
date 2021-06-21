from arXiv_info_receiving.src.data import download_data
from arXiv_info_receiving.src.add_to_db import to_db


path_json = "arxiv-metadata-oai-snapshot.json"
arxiv_df, set_id = download_data(path_json)


def test_info_first():
    url_test_eq = 'https://arxiv.org/abs/1706.03762'
    new_arxiv, new_set = to_db(arxiv_df, set_id, url_test_eq)
    assert len(new_arxiv) == len(arxiv_df)


def test_info_second():
    url_test_eq = 'http://www.africau.edu/images/default.pdfddddddd'
    new_arxiv, new_set = to_db(arxiv_df, set_id, url_test_eq)
    assert len(new_arxiv) == len(arxiv_df)

def test_info_three():
    url_test_greater = 'https://arxiv.org/abs/2105.14021v1'
    new_arxiv, new_test = to_db(arxiv_df, set_id, url_test_greater)
    assert len(new_arxiv) > len(arxiv_df)
