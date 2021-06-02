import pandas as pd
import arxiv


def get_info_arxiv(id_article: str):
    arxiv_dict = {}
    try:
        search = arxiv.Search(id_list=[id_article])
        paper = next(search.get())
    except (arxiv.arxiv.HTTPError, AttributeError):
        print("Check url")
        return None
    arxiv_dict['id'] = id_article
    arxiv_dict['submitter'] = None
    authors = ''
    for author in paper.authors:
        authors += str(author) + '\n'
    arxiv_dict['authors'] = authors
    arxiv_dict['title'] = paper.title
    arxiv_dict['comments'] = paper.comment
    arxiv_dict['journal_ref'] = paper.journal_ref
    arxiv_dict['doi'] = paper.doi
    arxiv_dict['report-no'] = None
    categories = ''
    for category in paper.categories:
        categories += str(category)
    arxiv_dict['categories'] = categories
    arxiv_dict['license'] = None
    arxiv_dict['abstract'] = paper.summary
    if isinstance(paper.updated.strftime("%Y-%m-%d"), str):
        arxiv_dict['update_date'] = paper.updated.strftime("%Y-%m-%d")
    else:
        arxiv_dict['update_date'] = paper.published.strftime("%Y-%m-%d")
    arxiv_df = pd.DataFrame(arxiv_dict, index=[0])
    return arxiv_df
