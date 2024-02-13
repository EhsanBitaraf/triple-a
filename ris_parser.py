

# file: Union[TextIO, Path],

#         with file.open(mode="r", newline=newline, encoding=encoding) as f:
#             return parser(**kw).parse_lines(f)


from triplea.schemas.article import Article, Author, Keyword


def parse_ris_block(lines):
    a = Article()
    a.OreginalArticle = {"file": lines}
    last_e=""
    print(f"#--------------------------------------------")
    # for line in lines:
    for l in range(0,len(lines)):
        line = lines[l]
        element_value = line.split("  - ")
        e = element_value[0]
        
        #--------------------UTF Clening-----------
        if str.__contains__(e,'\ufeff'):
            # UTF8
            e = str.replace(e,'\ufeff','')
        #--------------------UTF Clening-----------

        # ------------------------------Check
        if len(element_value) == 2:
            v = str.replace(element_value[1],'\n','').strip()
            last_e = e
            if v.__contains__('\n'):
                print("wow")
        else: # len split is 1
            if last_e == "": # First Line
                pass
            elif last_e == "N1":
                pass
            elif last_e == "KW":
                a.Keywords.append(Keyword(Text=v))
            elif last_e == "ER":
                pass
            elif last_e == "AD":
                pass
            elif last_e == "SN":
                pass
            elif last_e == "AB":  # Abstract or synopsis. Notes. Synonym of N2.
                a.Abstract =a.Abstract + ' ' + v
            elif last_e == "LA":
                pass
            else:
                print("-----------------------------")
                print(last_e)
                print(f"len : {len(element_value)} --> {line}")
                # print(lines)

            v = ""                      
        # ------------------------------Check
        # https://en.wikipedia.org/wiki/RIS_(file_format)
        if e == "TY": # Type of reference. Must be the first tag.
            pass
            # print(f"{e} -> {v}")        
            if v == "JOUR": # Journal Type
                pass
            elif v =="CONF": # Conference proceedings
                pass
            elif v =="CPAPER": # Conference paper
                pass
            elif v =="CHAP":  # Book section/chapter
                pass
            elif v =="BOOK":  # Book (whole)
                pass
            else:
                print(f"TY ---> {element_value[1]}")

        elif e == "TI": # (Primary) title, e.g. title of entry/grant/podcast/work, case name, or name of act.
            a.Title = v
            # print(f"{e} -> {v}")
        elif e == "T2":  # Secondary title, journal, periodical, publication title, code, title of weblog, series title, book title, image source program, conference name, dictionary title, periodical title, encyclopedia title, committee, program, title number, magazine, collection title, album title, newspaper, published 
            a.Journal = v
            print(f"{e} -> {v}")
            # All 
            # Nippon Ishikai zasshi. Journal of the Japan Medical Association  
            # Toshiba Review
            # IEEE Transactions on Components, Hybrids, and Manufacturing Technology
            # 2012 North American Power Symposium, NAPS 2012
            # J Med Internet Res
        elif e == "J2":  # Alternate title, e.g. alternate journal, abbreviated publication, abbreviation, or alternate magazine. If possible, it should be a standard abbreviation, preferably using the Index Medicus style including periods. This field is used for the abbreviated title of a book or journal name, the latter mapped to T2.
            pass
            print(f"{e} -> {v}") 
            # J2 -> Dianli Xitong Baohu yu Kongzhi
            # T2 -> Dianli Xitong Baohu yu Kongzhi/Power System Protection and Control  

            # J2 -> Rev. Educ.
            # T2 -> Review of Education        
        
        elif e == "AB":  # Abstract or synopsis.[6][14][8][15][17][18][19] Notes. Synonym of N2.
            a.Abstract = v
            # print(f"{e} -> {v}")
        elif e == "KW": # Keyword/phrase. Must be at most 255 characters long. May be repeated any number of times to add multiple keywords
            if a.Keywords is None:
                a.Keywords = []
            a.Keywords.append(Keyword(Text=v))
        elif e == "AU": # (Primary) author/editor/translator, e.g. author, artist, created by, attribution, programmer, investigators, editor, director, interviewee, cartographer, composer, reporter, inventor, or institution. The tag must be repeated for each person. Synonym of A1.
            if a.Authors is None:
                a.Authors = []
            a.Authors.append(Author(FullName=v))
            # All
            # print(f"{e} -> {v}")
        elif e == "A2":  # Secondary author/editor/translator, e.g. editor, performers, sponsor, series editor, reporter, institution, name of file, producer, series director, department, interviewer, issuing organization, recipient, or narrator. The tag must be repeated for each person. Synonym of 
            if a.Authors is None:
                a.Authors = []
            a.Authors.append(Author(FullName=v))
            # Not All
            # print(f"{e} -> {v}")
        elif e == "C2":  # Custom 2, e.g. PMCID, credits, year published, unit of observation, date cited, congress number, contact address, area, form of composition, issue, issue date, recieipients e-mail, or report number.[6][14][18][20]
            a.PMC = v
            # print(f"{e} -> {v}") 
            # PMC10770784
            # PMC10618876
        elif e == "C7":  # Custom 7, e.g. article number or PMCID.
            a.PMC = v # ?
            pass
            # 110170
            # 1333
            # 8847609
            # e94
            # print(f"{e} -> {v}")

        elif e == "DOI": # Digital Object Identifier (DOI)
            a.DOI = v
        elif e == "DO":  # Digital Object Identifier (DOI).
            a.DOI = v
        elif e == "LA":
            pass 
            # print(f"{e} -> {v}")
            # eng, English, Chinese
        elif e == "ST": # Short title or abbreviated case name
            pass
            # print(f"{e} -> {v}")
            # Like TI if other language
        elif e == "PY":  # (Primary) (publication) year/date, e.g. year decided, year of conference, or year released.[6][14][11][8][16][17][18][20] Must always use 4 digits, with leading zeros if before 1000.[6] Synonym of Y1.[8]
            pass
            # print(f"{e} -> {v}")   # All
            # 2012
            # 2023
        elif e == "YR":  # Publication year
            yr = v
            print(f"{e} -> {v}")
            # ?
        elif e == "DA":  # Date, e.g. date accessed, last update date, date decided, date of collection, date released, deadline, date of code edition, or date enacted.
            pass
            # print(f"{e} -> {v}") # Not All
            # Oct, Dec, May 27, MAR, Feb
        elif e == "SN":  # ISSN, ISBN, or report/document/patent number.
            pass
            # print(f"{e} -> {v}")
            # 16743415 (ISSN)
            # 1040-2446
            # 978-195591706-3 (ISBN)
            # 2212-1366 (Print)
            # 1099-4300 J9 - ENTROPY-SWITZ
            # 18761100 (ISSN); 978-981195537-2 (ISBN)
        elif e == "ER": # End of reference. Must be the last tag.
            pass
            # print(f"{e} -> {v}")
            # /n
        elif e == "DP":  # Database provider.
            pass
            # print(f"{e} -> {v}")
            # NLM
        elif e == "DB":  # Name of database.
            pass
            # print(f"{e} -> {v}")
            # Scopus 
        elif e == "AN":  # Accession number.
            pass
            # print(f"{e} -> {v}") 
            # WOS:000900130208031
            # 37847549
        elif e == "M3":  # Type of work, e.g. type (of work/article/medium/image); citation of reversal; medium; funding, patent, or thesis type; format; or form of item.[6][14][18][20] Miscellaneous 3.[9][22][8][17][18] Suitable to hold the medium.[8]
            pass
            # Not All
            # print(f"{e} -> {v}") 
            # Article
        elif e == "AD":  # (Author/editor/inventor) address, e.g. postal address, email address, phone number, and/or fax number.[6][14][9][21][8][15][18][19] Institution.[20]
            pass
            # All
            # print(f"{e} -> {v}")
            # This is Affiliation
            # EnBW Kernkraft GmbH, Philippsburg, Germany
            # University of Colorado Anschutz Medical Campus School of Medicine, Aurora, CO, USA.
            # Computer Science, Georgia Institute of Technology, Atlanta, USA.
        elif e == "ID":  # Reference identifier, may be limited to 20 alphanumeric characters.
            pass
            # print(f"{e} -> {v}")
            # ?
        elif e == "IS":  # Number, e.g. issue or number of volumes.
            pass
            # print(f"{e} -> {v}")
            # 18
            # 3
        elif e == "PB":  # Publisher, e.g. court, distributor, sponsoring agency, library/archive, assignee, institution, source, or university / degree grantor.
            pass
            # print(f"{e} -> {v}")
            # Institute of Electrical and Electronics Engineers Inc.
            # Association for Computational Linguistics (ACL)
            # IEEE Computer Society
        elif e == "N1":  # Notes.
            pass
            # print(f"{e} -> {v}") 
            # Export Date: 10 February 2024; Cited By: 2; 
            # Times Cited in Web of Science Core Collection: 0 Total Times Cited: 0 Cited Reference Count: 33
            # 2287-285x
            # Export Date: 10 February 2024; Cited By: 0; CODEN: ELKTA
        elif e == "SP":  # Pages, description, code pages, number of pages, first/start page, or running time.
            pass
            # print(f"{e} -> {v}") 
            # 261-270
            # e50865
            # e94
            # e12-e22
            # 105219
            # 239
        elif e == "T3":  # source, title of show, section title, academic department, or full journal name.
            pass
            # print(f"{e} -> {v}")
            # ?
        elif e == "VL":  # Volume, code volume, access year, reporter volume, image size, edition, amount requested, rule number, volume/storage container, number, patent version number, code number, or degree.
            pass
            # print(f"{e} -> {v}")
            # 2016-December
            # 52
            # 121
            # 5517 LNCS
             
        elif e == "UR":  # Web/URL. Can be repeated for multiple tags, or multiple URLs can be entered in the same tag as a semicolon-separated list.[6][9][22][8][15][16][17][18][19][20]
            pass
            # print(f"{e} -> {v}")
            # https://www.scopus.com/inward/record.uri?eid=2-s2.0-84961725690&doi=10.7667%2fPSPC151240&partnerID=40&md5=fa3bc7d65364213ec8ed9510f3a6da11


        elif e == "C6":  # Custom 6, e.g. NIHMSID, CFDA number, legal status, issue, or volume.[6][14][18][20]
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])  
            # ['C6', 'DEC 2023\n']
        elif e == "ET":  # Edition, e.g. epub (electronic publication?) date, date published, session, action of higher court, version, requirement, description of material, international patent classification, or description.[6][14][16][18][19][20]
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1]) 
            # ['ET', '2023/10/04\n'] 
        elif e == "OP":  #  Original publication, e.g. contents, history, content, version history, original grant number, or priority numbers.[6][14][18] Other pages.[15][20] Original foreign title.[15]
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])   
        elif e == "C3":  # Custom 3, e.g. size/length, title prefix, proceedings title, data type, PMCID, congress session, contact phone, size, music parts, or designated states.[6][14][18][20]
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])
        elif e == "SE":  #  Section, screens, code section, message number, pages, chapter, filed date, number of pages, original release date, version, e-pub date, duration of grant, section number, start page, international patent number, or running time.
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])                                               
        else:
            pass
            if len(e) > 2:
                pass
            else:
                pass
                if e != "\n":
                    print(e)

            

        
        # v = element_value [1]    

# with open("scopus.ris", encoding="utf8") as file:
with open("ris.ris", encoding="utf8") as file:
    lines = file.readlines()


# for l in lines:
#     parse_ris_line(l)
    

a_block = []
for i in range(0,len(lines) -1):
    a_block.append( lines[i])

    if lines[i][:5] == 'ER  -':
        parse_ris_block(a_block)
        a_block = []       

    # # One Method for Split Block
    # if lines[i] == "\n":
    #     if lines[i+1] == "\n":
    #         parse_ris_block(a_block)
    #         a_block = []
        






