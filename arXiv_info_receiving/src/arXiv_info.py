import arxiv
import logging


def get_info_arxiv(id_article: str) -> dict:
    global paper
    arxiv_dict = {}
    try:
        search = arxiv.Search(id_list=[id_article])
        paper = next(search.get())
    except (arxiv.arxiv.HTTPError, AttributeError):
        logging.warning("Check url")
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
    paper_updated = paper.updated.strftime("%Y-%m-%d")
    arxiv_dict['update_date'] = paper.updated.strftime("%Y-%m-%d") if isinstance(paper_updated, str) else \
        paper.published.strftime("%Y-%m-%d")
    return arxiv_dict
