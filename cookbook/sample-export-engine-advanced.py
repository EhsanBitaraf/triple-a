# sample-export-engine-advanced

# In this part, the export_engine function is used to get the output.
# For this purpose and getting the desired output, three functions
# fx_filter, fx_transform, and fx_output have been written.
# This example is tested on biobank data.
# In This example we use convert_unified2csv_dynamically function.

import json
import click
import pandas as pd
from triplea.schemas.article import Article
from triplea.service.repository.export.engine import export_engine
from triplea.service.repository.export.unified_export_json import json_converter_01
from triplea.service.repository.export.unified_export_json.convert import Converter
from triplea.utils.general import print_pretty_dict, safe_csv

def fx_filter(article:Article):
    return True
    for i in article.ReviewLLM:
        if i['TemplateID'] == "CardioBioBank1":
            if isinstance(i['Response'],dict):
                if 'Include' in i['Response']:
                    if i['Response']['Include'] is True:
                        return True
                else:
                    return False
            else:
                pass
                
    # Finally
    return False

def harmonization_string_field(f):
    if isinstance(f,str):
        output = []
        if f.__contains__(','):
            list_f = f.split(',')
            for i in list_f:
                output.append(safe_csv(i.strip()))
        elif f.__contains__(' or '):
            list_f = f.split(' or ')
            for i in list_f:
                output.append(safe_csv(i.strip()))
        elif f.__contains__(' and '):
            list_f = f.split(' and ')
            for i in list_f:
                output.append(safe_csv(i.strip()))
        else:        
            output = [safe_csv(f)]
    elif isinstance(f,list):
        output = f
    elif f is None:
        output = None
    else:
        # print()
        # print(f"in harmonization_string_field - {f} with type {type(f)} is unhandel.")
        output = ['Can not parse.']

    return output

def fx_transform(article:Article):
    # convert article info into unified format
    ainfo = json_converter_01(article)

    output = {}

    # General one to one info of article
    output['title'] = safe_csv(ainfo["title"])
    output['year'] = ainfo["year"]
    output['publisher'] = safe_csv(ainfo["publisher"])
    output['journal_issn'] = ainfo["journal_issn"]
    output['journal_iso_abbreviation'] = safe_csv(ainfo["journal_iso_abbreviation"])
    output['language'] = safe_csv(ainfo["language"])
    output['publication_type'] = safe_csv(ainfo["publication_type"])
    output['url'] = ainfo["url"]
    # output['abstract'] = safe_csv(ainfo["abstract"])
    output['doi'] = ainfo["doi"]
    output['pmid'] = ainfo["pmid"]
    output['state'] = ainfo["state"]
    output['citation_count'] = ainfo["citation_count"]

    # General one to many info of article
    output['authors'] = ainfo["authors"]
    
    list_keywords = []
    if ainfo["keywords"] is not None:
        for k in ainfo["keywords"]:
            list_keywords.append(safe_csv(k.Text))
    output['keywords'] = list_keywords
    list_topic = []
    if ainfo["topics"] is not None:
        for t in ainfo["topics"]:
            list_topic.append(safe_csv(t['text']))
    output['topics'] = list_topic


    # For T102
    output['A'] = None
    output['B'] = None
    output['C'] = None
    output['D'] = None
    output['E'] = None
    output['F'] = None
    # output['G'] = None
    output['T101_SP'] = None

    # For CardioBioBank1
    output['Include'] = None
    output['Biobanks'] = None
    output['Domain']= None
    output['Sample']= None
    output['CardioBioBank1_SP'] = None

    # Custom fields from LLM review
    for i in article.ReviewLLM:
        if i['TemplateID'] == "T102":
            r = i['Response']
            if 'StringContent' in r:
                output['T101_SP'] = 1
            else:
                if 'A' in r:
                    output['A'] = r['A']
                if 'B' in r:
                    output['B'] = r['B']
                if 'C' in r:
                    output['C'] = harmonization_string_field(r['C'])
                if 'D' in r:
                    output['D'] = harmonization_string_field(r['D'])
                if 'E' in r:
                    output['E'] = harmonization_string_field(r['E'])
                if 'F' in r:
                    if type(r['F']) is int:
                        output['F'] = r['F']
                    elif isinstance(r['F'],list):
                        sum_i =0 
                        for i in r['F']:
                            if isinstance(i,int):
                                sum_i = sum_i + i
                            else:
                                output['F'] = -2
                        output['F'] = sum_i
                    elif r['F'] is None:
                        output['F'] = None
                    else:
                        output['F'] = -1
                else:
                    r['F'] = None                   
                # if 'G' in r:
                #     output['G'] = safe_csv(r['G'])
                # else:
                #     output['G'] = ""

        elif i['TemplateID'] == "CardioBioBank1":
            r = i['Response']
            if 'StringContent' in r:
                output['CardioBioBank1_SP'] = 1
            else:
                output['Include'] = r['Include']
                if 'Biobanks' in r:
                    output['Biobanks'] = harmonization_string_field(r['Biobanks'])
                if 'Domain' in r:
                    output['Domain']= r['Domain']
                if 'Sample' in r:
                    output['Sample']= r['Sample']

    return output

def fx_output(output):
    if output !="":
        return output
    else:
        return ""


def detect_field_types(df):
    main_fields = []
    one_to_many_fields = []

    for column in df.columns:
        if df[column].apply(lambda x: isinstance(x, list)).all():
            one_to_many_fields.append(column)
        else:
            main_fields.append(column)

    return main_fields, one_to_many_fields


def convert_df2csv(df):
    main_fields, one_to_many_fields = detect_field_types(df)
    df = df.reset_index(drop=True)

    print("These are is main fields:")
    print(main_fields)

    print("These are one to many fields:")
    print(one_to_many_fields)

    # Create main CSV with explicit ID column
    main_df = df[main_fields].copy()
    main_df.insert(0, 'id', main_df.index)
    main_df.to_csv('main.csv', index=False)
    print("-- main.csv saved.")

    # Create separate CSV files for one-to-many fields
    for field in one_to_many_fields:
        rows = []
        for index, row in df.iterrows():
            for item in row[field]:
                rows.append({'id': index, field: item})
        pd.DataFrame(rows).to_csv(f'main_{field}.csv', index=False)
        print(f"-- main_{field}.csv saved.")



if __name__ == "__main__":
    ol = export_engine(fx_filter,fx_transform,fx_output,
                       limit_sample=0,
                       proccess_bar=False)
    print()
    print(f"{len(ol)} Articles selected and transform.")

    # General Model for convert - Old Version
    c = Converter()
    c.convert_unified2csv_dynamically(ol)

    # General Model for convert - New Version
    df = pd.DataFrame(ol)
    convert_df2csv(df)

    

