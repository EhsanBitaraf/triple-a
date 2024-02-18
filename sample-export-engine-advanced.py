# sample-export-engine-advanced

# In this part, the export_engine function is used to get the output.
# For this purpose and getting the desired output, three functions
# fx_filter, fx_transform, and fx_output have been written.
# This example is tested on biobank data.
# In This example we use convert_unified2csv_dynamically function.

import click
from triplea.schemas.article import Article
from triplea.service.repository.export.engine import export_engine
from triplea.service.repository.export.unified_export_json import json_converter_01
from triplea.service.repository.export.unified_export_json.convert import convert_unified2csv_dynamically
from triplea.utils.general import pretty_print_dict, safe_csv

def fx_filter(article:Article):
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
                # print()
                # print(type(i['Response']))
                
    # Finally
    return False

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
    output['abstract'] = safe_csv(ainfo["abstract"])
    output['doi'] = ainfo["doi"]
    output['pmid'] = ainfo["pmid"]
    output['state'] = ainfo["state"]
    output['citation_count'] = ainfo["citation_count"]

    # General one to many info of article
    output['authors'] = ainfo["authors"]
    output['keywords'] = ainfo["keywords"]
    output['topics'] = ainfo["authors"]

    # Custom fields from LLM review
    for i in article.ReviewLLM:
        if i['TemplateID'] == "T102":

            r = i['Response']
            if 'StringContent' in r:
                output['A'] = None
                output['B'] = None
                output['C'] = None
                output['D'] = None
                output['E'] = None
                output['F'] = None
                output['G'] = None
            else:
                output['A'] = r['A']
                output['B'] = r['B']
                if 'C' in r:
                    output['C'] = harmonization_string_field(r['C'])
                output['D'] = harmonization_string_field(r['D'])
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
                    # print()
                    # print("F Not Exist.")
                    # print(r)
                    r['F'] = None                   
                if 'G' in r:
                    pass
                    # output['G'] = r['G']
                    output['G'] = ""
                else:
                    # print()
                    # print("G Not Exist.")
                    # print(r)
                    output['G'] = ""

        elif i['TemplateID'] == "CardioBioBank1":
            r = i['Response']
            if 'StringContent' in r:
                output['Include'] = None
                output['Biobanks'] = None
                output['Domain']= None
                output['Sample']= None
            else:
                output['Include'] = r['Include']
                output['Biobanks'] = harmonization_string_field(r['Biobanks'])
                output['Domain']= r['Domain']
                if 'Sample' in r:
                    output['Sample']= r['Sample']

    # print(output)
    return output

def fx_output(output):
    if output !="":
        return output
    else:
        return ""

def convert2csv(list_output):
    main_csv = "ID,Arxive,PMID,A,B,F,Description,Include,Sample\n"
    main_c = "ID,BioBank\n"
    main_d = "ID,Medical Domain\n"
    main_e = "ID,BioBank Domain\n"
    main_biobanks="ID,BioBanks\n"
    main_domain="ID,ICD,ICD_Code\n"

    with open("main.csv", "w", encoding="utf-8") as file1:
        file1.write(main_csv)
    with open("main_c.csv", "w", encoding="utf-8") as file1:
        file1.write(main_c)
    with open("main_d.csv", "w", encoding="utf-8") as file1:
        file1.write(main_d)
    with open("main_e.csv", "w", encoding="utf-8") as file1:
        file1.write(main_e) 
    with open("main_biobanks.csv", "w", encoding="utf-8") as file1:
        file1.write(main_biobanks) 
    with open("main_domain.csv", "w", encoding="utf-8") as file1:
        file1.write(main_domain) 
    csv = ""
    main_c =""
    main_d = ""
    main_e = ""
    main_biobanks=""
    main_domain=""

    f_main = open("main.csv", "a", encoding="utf-8")  
    f_main_c = open("main_c.csv", "a", encoding="utf-8")    
    f_main_d = open("main_d.csv", "a", encoding="utf-8")  
    f_main_e = open("main_e.csv", "a", encoding="utf-8") 
    f_main_biobanks=open("main_biobanks.csv", "a", encoding="utf-8") 
    f_main_domain=open("main_domain.csv", "a", encoding="utf-8") 

    for i in range(0,len(list_output)):
        r = list_output[i]
        if 'F' in r:
            if r['F'] is None:
                F = ""
            else:
                F = r['F']
        else:
            F = ""
        if 'Sample' in r:
            if r['Sample'] is None:
                sample = ""
            else:
                sample = r['Sample']
        else:
            sample = ""
        
        
        csv = csv + f"{str(i)},{safe_csv(r['ArxivID'])},{safe_csv(r['PMID'])},{r['A']},{r['B']},{F},{safe_csv(r['G'])},{r['Include']},{sample}\n"
        f_main.write(csv)
        csv = ""
        if r['C'] is not None:
            for C in r['C']:
                C = C.lower()
                C = str.replace( C,')','')
                main_c = main_c + f"{str(i)},{safe_csv(C)}\n"
                f_main_c.write(main_c)
                main_c = ""
        if r['D'] is not None:
            for D in r['D']:
                D = D.lower()
                D = str.replace(D,'medical research (','')
                D = str.replace( D,')','')
                main_d = main_d + f"{str(i)},{safe_csv(D)}\n"
                f_main_d.write(main_d)
                main_d = ""
        if r['E'] is not None:
            for E in r['E']:
                main_e = main_e + f"{str(i)},{safe_csv(E)}\n"
                f_main_e.write(main_e)
                main_e = ""

        if r['Biobanks'] is not None:
            for E in r['Biobanks']:
                main_biobanks = main_biobanks + f"{str(i)},{safe_csv(E)}\n"
                f_main_biobanks.write(main_biobanks)
                main_biobanks = ""

        if r['Domain'] is not None:
            for E in r['Domain']:
                if 'code' in E:
                    pass
                else:
                    E['code'] = ""
                main_domain = main_domain + f"{str(i)},{safe_csv(E['value'])},{safe_csv(E['code'])}\n"
                f_main_domain.write(main_domain)
                main_domain = ""

    f_main.close()
    f_main_c.close()
    f_main_d.close()
    f_main_e.close()
    f_main_biobanks.close()
    f_main_domain.close()

if __name__ == "__main__":
    ol = export_engine(fx_filter,fx_transform,fx_output,limit_sample=0)
    print()
    print(f"{len(ol)} Articles selected and transform.")

    # # Text Base File
    # f = open("outputfile.txt", "a")
    # for o in ol:
    #     if o is not None:
    #         if o != "":
    #             f.write(f"{o}\n")
    # f.close()
    
    # # Writing to sample.json
    # json_object = json.dumps(list_output, indent=4)
    # with open("outputfile.json", "w") as outfile:
    #     outfile.write(json_object)

    # # Convert Json Model To Multiple CSV file
    # convert2csv(ol)

    # Convert Json Model To Multiple CSV file
    convert_unified2csv_dynamically(ol)

    

