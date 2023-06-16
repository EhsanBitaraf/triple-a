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


def _is_university(txt:str):
    if txt.lower().__contains__("university"):
        return True
    else:
        return False
    
def _is_center(txt:str):
    if txt.lower().__contains__("center"):
        return True
    else:
        return False
    
def _is_department(txt:str):
    if txt.lower().__contains__("department"):
        return True
    else:
        return False

def _is_institute(txt:str):
    if txt.lower().__contains__("institute"):
        return True
    else:
        return False

def _is_hospital(txt:str):
    if txt.lower().__contains__("hospital"):
        return True
    else:
        return False
    
def _is_country(txt:str):
    if country_list.__contains__(txt):
        return True
    else:
        return False  

def affiliation_mining(article: Article):
    article.FlagAffiliationMining = 0 # Critical
    if article.Authors is not None:
        for a in article.Authors:
            if a.Affiliations is not None:
                for aff in a.Affiliations:
                    # print()
                    # print(aff.Text)
                    aff_part = aff.Text.split(",")
                    aff_part_number = len(aff_part)
                    loc = []
                    n=0
                    for p in aff_part:
                        
                        if _is_university(p):
                            loc.append({ "university" : p.strip()})
                            n = n + 1
                        elif _is_center(p):
                            loc.append({ "center" : p.strip()})
                            n = n + 1
                        elif _is_department(p):
                            loc.append({ "department" : p.strip()})
                            n = n + 1
                        elif _is_institute(p):
                            loc.append({ "institute" : p.strip()})
                            n = n + 1
                        elif _is_hospital(p):
                            loc.append({ "hospital" : p.strip()})
                            n = n + 1
                        elif _is_country(p.replace('.', '').strip()):
                            loc.append({ "country" : p.replace('.', '').strip()})
                            n = n + 1
                        else:
                            pass
                            # print(p)
                    if aff_part_number - n > 3:
                        print()
                        print(loc)
                        print(aff.Text)
                        print(aff_part_number - n)





def affiliation_mining1(article: Article):
    article.FlagAffiliationMining = 0 # Critical
    if article.Authors is not None:
        for a in article.Authors:
            if a.Affiliations is not None:
                for aff in a.Affiliations:
                    # print(aff.Text)
                    aff_part = aff.Text.split(",")
                    aff_part_number = len(aff_part)
                    if aff_part_number > 3:
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

                    else: # aff_part_number < 3
                        pass







    return article