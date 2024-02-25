from triplea.schemas.article import Article
from triplea.service.repository.export.engine import export_engine
from triplea.service.repository.export.unified_export_json.convert import Converter



def harmonization_string_field(f):
    if isinstance(f,str):
        output = []
        if f.__contains__(','):
            list_f = f.split(',')
            for i in list_f:
                output.append(i.strip())
        elif f.__contains__(' or '):
            list_f = f.split(' or ')
            for i in list_f:
                output.append(i.strip())
        elif f.__contains__(' and '):
            list_f = f.split(' and ')
            for i in list_f:
                output.append(i.strip())          
        else:        
            output = [f]
    elif isinstance(f,list):
        output = f
    elif f is None:
        output = None
    else:
        # print()
        # print(f"{f} with type {type(f)}")
        return ""
    return output


def fx_filter(article:Article):
    for i in article.ReviewLLM:
        if i['TemplateID'] == "T102":
            return True

def fx_transform(article:Article):
    output = {}
    output['pmid'] = article.PMID
    for i in article.ReviewLLM:
        if i['TemplateID'] == "T102":
            r = i['Response']
            if 'StringContent' in r:
                output['C'] = None
                output['T102_StringContent'] = True
                # if 'ErrorMsg' in r:
                #     output['ErrorMsg'] = r['ErrorMsg']
                # else:
                #     output['ErrorMsg'] = None
            else: # Is not StringContent
                if 'C' in r:
                    output['C'] = harmonization_string_field(r['C'])
                    output['T102_StringContent'] = False
                    # output['ErrorMsg'] = None
                else:
                    output['C'] = None
                    output['T102_StringContent'] = False
                    # output['ErrorMsg'] = None
        elif i['TemplateID'] == "CardioBioBank1":
            output['Has_Biobank2'] = 1
            r = i['Response']
            if isinstance(r,str):
                # khataye fahesh update man
                output['CardioBioBank1_StringContent'] = True

            else:
                if 'StringContent' in r:
                    output['Biobank2'] = None
                    output['CardioBioBank1_StringContent'] = True
                    # if 'ErrorMsg' in r:
                    #     output['ErrorMsg'] = r['ErrorMsg']
                    # else:
                    #     output['ErrorMsg'] = None
                else: # Is not StringContent
                    output['Include'] = r['Include']
                    output['Biobank2'] = harmonization_string_field(r['Biobanks'])
                    output['CardioBioBank1_StringContent'] = False    
                    # output['ErrorMsg'] = None     
                

    return output

def fx_output(output):
    if output !="":
        return output
    else:
        return ""

if __name__ == "__main__":
    ol = export_engine(fx_filter,fx_transform,fx_output,limit_sample=0,proccess_bar=False)
    print()
    print(f"{len(ol)} Articles selected and transform.")

    # General Model
    c = Converter()
    c.convert_unified2csv_dynamically(ol)