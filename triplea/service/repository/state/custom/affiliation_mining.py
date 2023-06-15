import sys
from triplea.schemas.article import Article
from triplea.service.click_logger import logger
from triplea.service.nlp.triple_extract import extract_triples
import triplea.service.repository.persist as persist
from triplea.config.settings import ROOT

country_list = []

f = open(ROOT.parent / 'datasets'  / 'country.txt')
count = 0
while True:
    count += 1
    line = f.readline()
    country_list.append(line.strip())
    if not line:
        break


def _is_email(txt:str) -> bool:
    if txt.__contains__('@'):
        return True
    else:
        return False
    
def _has_numbers(txt:str):
    return any(char.isdigit() for char in txt)

def affiliation_mining(article: Article):
    article.FlagAffiliationMining = 0 # Critical

    for a in article.Authors:
        if a.Affiliations is not None:
            for aff in a.Affiliations:
                # print(aff.Text)

                aff_part = aff.Text.split(",")
                aff_part_number = len(aff_part)
                end_pointer =  1 
                country = aff_part[aff_part_number - (end_pointer)]

                if _is_email(country):
                    email = country
                    end_pointer =  end_pointer + 1
                    usename = email.split("@")[0]
                    if usename.__contains__(' '):
                        # print("مشکل")
                        country = "USA" # Critical بعدا درست می کنم
                    else:
                        country = aff_part[aff_part_number - (end_pointer)]
                    # print(email)
                    


                city = aff_part[aff_part_number - (end_pointer + 1)]


                country = country.replace('.', '')
                country = country.strip()
                if country_list.__contains__(country):
                    pass
                else:
                    if _has_numbers(country):
                        pass
                    else:
                        print()
                        print(f'Country : {country}') 
                        print(aff.Text)               

                # print(f'City : {city}')
                part3 = aff_part[aff_part_number - (end_pointer + 2)]
                # print(f'p3 : {part3}')
                if part3.__contains__('University'):
                    university = part3
                elif part3.__contains__('Hospital'):
                    hospital = part3
                elif part3.__contains__('Institute'):
                    institute = part3
                else:
                    pass
                    # print()
                    # print(aff.Text)
                    # raise NotImplementedError

                







    return article