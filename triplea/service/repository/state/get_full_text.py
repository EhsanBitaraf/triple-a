import os
from triplea.client.arxiv import get_pdf_by_arxiv_id
from triplea.schemas.article import Article, SourceBankType
import io
import PyPDF2
from triplea.config.settings import SETTINGS

from triplea.utils.general import print_error


def _get_full_text_pubmed(article: Article):
    raise NotImplementedError


def _get_full_text_arxiv(article: Article):
    if article.ArxivID is None:
        raise Exception("ArxivID is None")
    pdf_bytes = get_pdf_by_arxiv_id(article.ArxivID)
    if SETTINGS.AAA_FULL_TEXT_REPO_TYPE == "Directory":
        filename = f"{article.ArxivID}.pdf"
        if os.path.isdir(SETTINGS.AAA_FULL_TEXT_DIRECTORY) is False:
            os.mkdir(SETTINGS.AAA_FULL_TEXT_DIRECTORY)
        f = open(os.path.join(SETTINGS.AAA_FULL_TEXT_DIRECTORY, filename), "wb")
        f.write(pdf_bytes)
        f.close()
    elif SETTINGS.AAA_FULL_TEXT_REPO_TYPE == "Database":
        raise NotImplementedError
    else:
        raise NotImplementedError

    return article

    # Assume that the pdf bytes are stored in a variable called pdf_bytes
    pdf_stream = io.BytesIO(pdf_bytes)
    pdf_reader = PyPDF2.PdfReader(pdf_stream)
    print(pdf_reader.pages)
    print(len(pdf_reader.pages))
    print(pdf_reader.metadata)

    pdf_text = ""
    for p in pdf_reader.pages:
        print(type(p))
        text = p.extract_text()
        print(type(text))
        print(p.extract_text())
        pdf_text = pdf_text + " " + text

    f = open(f"{article.ArxivID}.txt", "w")
    f.write(pdf_text)
    f.close()

    pass


def get_full_text(article: Article):
    # previous state is 3
    article.State = 4  # next state
    backward_state = -3
    try:
        if article.SourceBank is None:
            # This is Pubmed
            updated_article = _get_full_text_pubmed(article)
        elif article.SourceBank == SourceBankType.PUBMED:
            updated_article = _get_full_text_pubmed(article)
        elif article.SourceBank == SourceBankType.ARXIV:
            updated_article = _get_full_text_arxiv(article)
        else:
            raise NotImplementedError
    except Exception:
        print_error()
        updated_article.State = backward_state

    return updated_article
