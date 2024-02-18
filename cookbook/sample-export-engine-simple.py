from triplea.schemas.article import Article
from triplea.service.repository.export.engine import export_engine


def fx_filter(article:Article):
    for i in article.ReviewLLM:
        if i['TemplateID'] == "Ass11":
            return True
    # Finally
    return False


def fx_transform(article:Article):
    for i in article.ReviewLLM:
        if i['TemplateID'] == "Ass11":
            if 'D' in i['Response']:
                return { "Out" : i['Response']['D'] }

    return ""
    
def fx_output(output):
    if 'Out' in output:
        return output['Out']

if __name__ == "__main__":
    ol = export_engine(fx_filter,fx_transform,fx_output,limit_sample=100)
    f = open("outputfile.txt", "a")
    for o in ol:
        if o is not None:
            if o != "":
                f.write(f"{o}\n")
    f.close()