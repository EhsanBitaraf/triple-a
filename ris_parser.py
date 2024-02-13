

# file: Union[TextIO, Path],

#         with file.open(mode="r", newline=newline, encoding=encoding) as f:
#             return parser(**kw).parse_lines(f)


from triplea.schemas.article import Article, Author, Keyword


def parse_ris_line(lines:str):
    a = Article()
    last_e=""
    # for line in lines:
    for l in range(0,len(lines)):
        line = lines[l]
        element_value = line.split("  - ")
        e = element_value[0]


# ------------------------------Check
        if len(element_value) == 2:
            v = element_value[1].replace(element_value[1],'\n').strip()
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
            elif e == "AB":  # Abstract or synopsis. Notes. Synonym of N2.
                a.Abstract =a.Abstract + ' ' + v
            else:
                print(last_e)
                print(f"len : {len(element_value)} --> {line}")
                print(lines)

            v = ""                      
# ------------------------------Check
                



        if e == "TY": # Type of reference. Must be the first tag.
            pass
            # if v == "JOUR":
            #     print(v)
            #     print(f"This is Journal")
            #     # print(f"Is Not Journal Type. It is {v}")
            # elif v =="":
            #     pass
            # else:
            #     print(f"TY ---> {element_value[1]}")
            
            
        elif e == "DOI": # Digital Object Identifier (DOI)
            a.DOI = v
        elif e == "DO":  # Digital Object Identifier (DOI).
            a.DOI = v
        elif e == "LA":
            pass
            # print(element_value[1])
        elif e == "KW": # Keyword/phrase. Must be at most 255 characters long. May be repeated any number of times to add multiple keywords
            if a.Keywords is None:
                a.Keywords = []
            a.Keywords.append(Keyword(Text=v))
        elif e == "ST": # Short title or abbreviated case name
            pass
        elif e == "TI": # (Primary) title, e.g. title of entry/grant/podcast/work, case name, or name of act.
            a.Title = v
        elif e == "YR":  # Publication year
            yr = v
        elif e == "DA":  # Date, e.g. date accessed, last update date, date decided, date of collection, date released, deadline, date of code edition, or date enacted.
            da = v
            # print(da)
        elif e == "ER": # End of reference. Must be the last tag.
            pass
        elif e == "SN":  # ISSN, ISBN, or report/document/patent number.
            pass
        elif e == "AB":  # Abstract or synopsis.[6][14][8][15][17][18][19] Notes. Synonym of N2.
            a.Abstract = v
        elif e == "DP":  # Database provider.
            pass
            # print(v)
        elif e == "DB":  # Name of database.
            pass
            # print(line)       
        elif e == "AU": # (Primary) author/editor/translator, e.g. author, artist, created by, attribution, programmer, investigators, editor, director, interviewee, cartographer, composer, reporter, inventor, or institution. The tag must be repeated for each person. Synonym of A1.
            if a.Authors is None:
                a.Authors = []
            a.Authors.append(Author(FullName=v))
        elif e == "AD":  # (Author/editor/inventor) address, e.g. postal address, email address, phone number, and/or fax number.[6][14][9][21][8][15][18][19] Institution.[20]
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])
        elif e == "ID":  # Reference identifier, may be limited to 20 alphanumeric characters.
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])
        elif e == "IS":  # Number, e.g. issue or number of volumes.
            pass
        elif e == "PB":  # Publisher, e.g. court, distributor, sponsoring agency, library/archive, assignee, institution, source, or university / degree grantor.
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])
        elif e == "C7":  # Custom 7, e.g. article number or PMCID.
            a.PMC = v
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])    
        elif e == "N1":  # Notes.
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])  
        elif e == "PY":  # (Primary) (publication) year/date, e.g. year decided, year of conference, or year released.[6][14][11][8][16][17][18][20] Must always use 4 digits, with leading zeros if before 1000.[6] Synonym of Y1.[8]
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])   
        elif e == "A2":  # Secondary author/editor/translator, e.g. editor, performers, sponsor, series editor, reporter, institution, name of file, producer, series director, department, interviewer, issuing organization, recipient, or narrator. The tag must be repeated for each person. Synonym of 
            if a.Authors is None:
                a.Authors = []
            a.Authors.append(Author(FullName=v)) 
        elif e == "AN":  # Accession number.
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])
            # WOS:000900130208031
            # 37847549
        elif e == "M3":  # Type of work, e.g. type (of work/article/medium/image); citation of reversal; medium; funding, patent, or thesis type; format; or form of item.[6][14][18][20] Miscellaneous 3.[9][22][8][17][18] Suitable to hold the medium.[8]
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])
            # Article


        elif e == "SP":  # Pages, description, code pages, number of pages, first/start page, or running time.
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])   

        elif e == "T2":  # Secondary title, journal, periodical, publication title, code, title of weblog, series title, book title, image source program, conference name, dictionary title, periodical title, encyclopedia title, committee, program, title number, magazine, collection title, album title, newspaper, published 
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])   

        elif e == "T3":  # source, title of show, section title, academic department, or full journal name.
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])                           

        elif e == "VL":  # Volume, code volume, access year, reporter volume, image size, edition, amount requested, rule number, volume/storage container, number, patent version number, code number, or degree.
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])   
        elif e == "UR":  # Web/URL. Can be repeated for multiple tags, or multiple URLs can be entered in the same tag as a semicolon-separated list.[6][9][22][8][15][16][17][18][19][20]
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1])
            # https://www.scopus.com/inward/record.uri?eid=2-s2.0-84961725690&doi=10.7667%2fPSPC151240&partnerID=40&md5=fa3bc7d65364213ec8ed9510f3a6da11
        elif e == "J2":  # Alternate title, e.g. alternate journal, abbreviated publication, abbreviation, or alternate magazine. If possible, it should be a standard abbreviation, preferably using the Index Medicus style including periods. This field is used for the abbreviated title of a book or journal name, the latter mapped to T2.
            pass
            # print(v)
            # print(element_value)
            # print(element_value[1]) 

        elif e == "C2":  # Custom 2, e.g. PMCID, credits, year published, unit of observation, date cited, congress number, contact address, area, form of composition, issue, issue date, recieipients e-mail, or report number.[6][14][18][20]
            a.PMC = v
            # ['C2', 'PMC10770784\n']

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
        elif e == "":  # 
            pass
            print(v)
            print(element_value)
            print(element_value[1])   
        elif e == "":  # 
            pass
            print(v)
            print(element_value)
            print(element_value[1])                                       
        else:
            pass
            if len(e) > 2:
                pass
            else:
                pass
                if e != "\n":
                    print(e)

            

        
        # v = element_value [1]    


with open("ris.ris") as file:
    lines = file.readlines()


# for l in lines:
#     parse_ris_line(l)
    

a_block = []
for i in range(0,len(lines) -1):
    a_block.append ( lines[i])
    if lines[i] == "\n":
        if lines[i+1] == "\n":
            parse_ris_line(a_block)
            a_block = []
        






