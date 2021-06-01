import time
from arXiv_info import get_info_arxiv
from data import download_data


if __name__ == '__main__':
    path_json = "arxiv-metadata-oai-snapshot.json"

    arxiv_df, set_id = download_data(path_json)
    url_list = ['https://arxiv.org/abs/1706.03762', 'https://arxiv.org/abs/2105.14021v1',
                'http://www.africau.edu/images/default.pdfddddddd', 'arxiv.orgaasd', 'https://arxiv.org/abs/9999.99999',
                'https://arxiv.org/abs/2105.14021v5', 'https://arxiv.org/abs/2105.14021v2',
                'https://arxiv.org/abs/2105.14021', 'https://arxiv.org/abs/1706.03762',
                'https://arxiv.org/abs/0704.0001']

    for url_article in url_list:
        if 'arxiv.org' in url_article:
            id_url = url_article.split('/')[-1]
            if 'v' in id_url:
                id_url = id_url[:-2]
            if id_url not in set_id:
                arxiv_data = get_info_arxiv(id_url)
                arxiv_df = arxiv_df.append(arxiv_data, ignore_index=True)
                set_id.add(id_url)
                time.sleep(3)
            else:
                print("This article already in database")
        else:
            print("This url not from arXiv")
    print(arxiv_df.shape)
    print(arxiv_df[-5:][['id', 'title']])
