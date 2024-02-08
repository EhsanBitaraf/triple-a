from triplea.schemas.article import Article
import triplea.service.llm as LLM_fx
from triplea.utils.general import print_error


def short_review_article(article: Article, article_id):
    article.FlagShortReviewByLLM = 1
    try:
        if article.Abstract is None:
            article.Abstract = ""

        r = LLM_fx.question_with_template_for_llm(article.Title, article.Abstract)
        if article.ReviewLLM is None:
            article.ReviewLLM = [r]
        else:
            article.ReviewLLM.append(r)
    except Exception:
        article.FlagShortReviewByLLM = -1
        print_error()

    return article
