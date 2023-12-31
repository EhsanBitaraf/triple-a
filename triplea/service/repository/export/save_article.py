import json

from triplea.schemas.article import Article
from triplea.utils.general import JSONEncoder


def save_article2json(article: Article, output_file: str):
    article_json = json.loads(
        json.dumps(article, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    )
    f = open(output_file, "w", encoding="utf-8")
    f.write(article_json)
    f.close()


def save_articlestr2json(article: dict, output_file: str):
    json_object = json.dumps(article, cls=JSONEncoder, indent=4)
    f = open(output_file, "w", encoding="utf-8")
    f.write(json_object)
    f.close()
