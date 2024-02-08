import os
from triplea.config.settings import SETTINGS
from triplea.schemas.article import Article, SourceBankType
from triplea.utils.general import print_error
import io

AAA_FULL_TEXT_CONVERTER_TYPE = "unstructured"


def _pypdf_page_cleaner(page):
    p1 = page.extract_text()
    p1 = p1.replace("-\n", " ")
    sen = p1.split("\n")

    for line in range(len(sen)):

        if line > 10 and len(sen[line]) > 1:
            # this for title end author name
            len_line = len(sen[line])

            lastch = sen[line][-1]
            if line + 1 != len(sen):
                try:
                    if len_line > 15 and len(sen[line + 1]) > 15 and lastch != ".":
                        new = sen[line].replace("\n", " ") + sen[line + 1]
                        sen[line] = new
                        sen[line + 1] = ""
                except Exception:
                    print(line)
                    print(len(sen))
                    raise


def _convert_pdf2string(pdf_bytes):
    if AAA_FULL_TEXT_CONVERTER_TYPE == "pypdf":
        # from pypdf import PdfReader
        import PyPDF2

        # Assume that the pdf bytes are stored in a variable called pdf_bytes
        pdf_stream = io.BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_stream)
        pdf_text = ""
        for p in pdf_reader.pages:
            text = p.extract_text()
            text = _pypdf_page_cleaner(p)
            pdf_text = pdf_text + " " + text

        return pdf_text

    elif AAA_FULL_TEXT_CONVERTER_TYPE == "unstructured":
        from unstructured.partition.auto import partition

        # filename = "2310.15773v1.pdf"
        # with open(filename, "rb") as f:
        #     elements = partition(file=f, include_page_breaks=True)

        pdf_stream = io.BytesIO(pdf_bytes)
        elements = partition(file=pdf_stream, include_page_breaks=True)

        full_text_string = ""
        for e in elements:
            full_text_string = full_text_string + e.text

        return full_text_string
    else:
        raise Exception("CONVERTER_TYPE is unknown.")


def _convert_full_text2string_pubmed(article: Article):
    raise NotImplementedError


def _convert_full_text2string_arxiv(article: Article):
    if SETTINGS.AAA_FULL_TEXT_REPO_TYPE == "Directory":
        filepath = os.path.join(
            SETTINGS.AAA_FULL_TEXT_DIRECTORY, f"{article.ArxivID}.pdf"
        )

        if os.path.isfile(filepath) is False:
            raise Exception(f"Full text file ({filepath}) not found.")
        with open(filepath, "rb") as f:
            pdf_bytes = f.read()

        fstr = _convert_pdf2string(pdf_bytes)
        tokens = len(fstr.split(" "))
        if SETTINGS.AAA_FULL_TEXT_STRING_REPO_TYPE == "Database":
            article.FullTextMetadata = {
                "ConverterType": AAA_FULL_TEXT_CONVERTER_TYPE,
                "String": fstr,
                "TokenCount": tokens,
            }
        elif SETTINGS.AAA_FULL_TEXT_STRING_REPO_TYPE == "Directory":
            filepath = os.path.join(
                SETTINGS.AAA_FULL_TEXT_STRING_DIRECTORY, f"{article.ArxivID}.txt"
            )
            f = open(filepath, "w")
            f.write(fstr)
            f.close()
            article.FullTextMetadata = {
                "ConverterType": AAA_FULL_TEXT_CONVERTER_TYPE,
                "TokenCount": tokens,
            }

        return article

    elif SETTINGS.AAA_FULL_TEXT_REPO_TYPE == "Database":
        raise NotImplementedError
    else:
        raise NotImplementedError


def convert_full_text2string(article: Article):
    # previous state is 4
    article.State = 5  # next state
    backward_state = -4
    try:
        if article.SourceBank is None:
            # This is Pubmed
            updated_article = _convert_full_text2string_pubmed(article)
        elif article.SourceBank == SourceBankType.PUBMED:
            updated_article = _convert_full_text2string_pubmed(article)
        elif article.SourceBank == SourceBankType.ARXIV:
            updated_article = _convert_full_text2string_arxiv(article)
        else:
            raise NotImplementedError
    except Exception:
        print_error()
        updated_article.State = backward_state

    return updated_article
