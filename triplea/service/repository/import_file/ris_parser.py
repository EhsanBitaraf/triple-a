# flake8: noqa
from time import sleep
from triplea.schemas.article import Article, Author, Keyword, SourceBankType
import triplea.service.repository.persist as PERSIST
from triplea.service.click_logger import logger
from triplea.utils.general import get_tqdm

def _parse_ris_block(lines, sourcebanktype=SourceBankType.UNKNOWN):
    debug = False
    a = Article()
    a.OreginalArticle = {"file": lines}
    a.InsertType = ["From RIS"]
    a.ReferenceCrawlerDeep = 0
    a.CiteCrawlerDeep = 0
    a.State = 2
    a.SourceBank = sourcebanktype
    last_e = ""
    if debug: print(f"#--------------------------------------------")
    C3 = ""
    # for line in lines:
    unknown_tag_list = []
    ptype_list = []
    for l in range(0, len(lines)):
        line = lines[l]
        element_value = line.split("  - ")
        e = element_value[0]

        # --------------------UTF Cleaning-----------
        if str.__contains__(e, "\ufeff"):
            # UTF8
            e = str.replace(e, "\ufeff", "")
        # --------------------UTF Cleaning-----------

        # ------------------------------Check for line without tag (in endnote)
        if len(element_value) == 2:
            v = str.replace(element_value[1], "\n", "").strip()
            last_e = e
            if v.__contains__("\n"):
                print("wow")
        else:  # len split is 1
            if last_e == "":  # First Line
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
                a.Abstract = a.Abstract + " " + v
            elif last_e == "LA":
                pass
            else:
                print("-----------------------------")
                print(last_e)
                print(f"len : {len(element_value)} --> {line}")
                # print(lines)

            v = ""
        # ------------------------------Check for line without tag (in endnote)


        
        # ------------------------------Parse all tag we need-----------------
        # https://en.wikipedia.org/wiki/RIS_(file_format)
        if e == "TY":  # Type of reference. Must be the first tag.
            pass
            # print(f"{e} -> {v}")
            if v == "JOUR":  # Journal Type
                pass
            elif v == "CONF":  # Conference proceedings
                pass
            elif v == "CPAPER":  # Conference paper
                pass
            elif v == "CHAP":  # Book section/chapter
                pass
            elif v == "BOOK":  # Book (whole)
                pass
            else:
                print(f"Value of TY Tag is unknown ---> {element_value[1]}")
            ptype_list.append(v)
        elif (e == "M3"):  
            # Type of work, e.g. type (of work/article/medium/image);
            #  citation of reversal; medium; funding, patent, or thesis type;
            #  format; or form of item. Miscellaneous 3.
            #  Suitable to hold the medium.
            pass
            ptype_list.append(v)
            # if debug: print(f"{e} -> {v}")
            # Article
        elif (e == "TI"):  
            # (Primary) title, e.g. title of entry/grant/podcast/work,
            #  case name, or name of act.
            a.Title = v
            # print(f"{e} -> {v}")
        elif (e == "T1"): # (Primary) title. 
            a.Title = v
            # T1 -> Current EHR developments: An Australian and international perspective - Part 1
        elif (e == "T2"):  
            # Secondary title, journal, periodical, publication title,
            #  code, title of weblog, series title, book title,
            #  image source program, conference name, dictionary title,
            #  periodical title, encyclopedia title, committee, program,
            #  title number, magazine, collection title, album title,
            #  newspaper, published
            a.Journal = v
            # print(f"{e} -> {v}")
            # All
            # Nippon Ishikai zasshi. Journal of the Japan Medical Association
            # Toshiba Review
            # IEEE Transactions on Components, Hybrids, and Manufacturing Technology
            # 2012 North American Power Symposium, NAPS 2012
            # J Med Internet Res
        elif (e == "JF"): # Full name of journal/periodical
            a.Journal = v
        elif (e == "JO"): 
            # Abbreviation (for journal/periodical name).
            #  "Periodical name: full format. This is an alphanumeric field
            #  of up to 255 characters."
            if debug : print(f"{e} -> {v}")
            # JO -> Healthc. Rev. Online
        elif (e == "JA"): 
            # Standard abbreviation for journal/periodical name.
            if debug : print(f"{e} -> {v}")
            # in IEEE
            # JA -> 2022 IEEE 19th International Conference on Software Architecture (ICSA)
        elif (e == "J2"):  
            # Alternate title, e.g. alternate journal,
            #  abbreviated publication, abbreviation,
            #  or alternate magazine. If possible,
            #  it should be a standard abbreviation,
            #  preferably using the Index Medicus style including periods.
            #  This field is used for the abbreviated title of a book
            #  or journal name, the latter mapped to T2.
            pass
            if debug : print(f"{e} -> {v}")
            # J2 -> Dianli Xitong Baohu yu Kongzhi
            # T2 -> Dianli Xitong Baohu yu Kongzhi/Power System Protection and Control
            # J2 -> Rev. Educ.
            # T2 -> Review of Education
            # J2 -> Medical teacher
            # T2 -> Med Teach

        elif (e == "AB"): 
            # Abstract or synopsis.Notes. Synonym of N2.
            a.Abstract = v
            # print(f"{e} -> {v}")
        elif (e == "N2"): 
            # Abstract. Synonym of AB.
            a.Abstract = v
            # print(f"{e} -> {v}")

        elif (e == "KW"):  
            # Keyword/phrase. Must be at most 255 characters long.
            #  May be repeated any number of times to add multiple keywords
            if a.Keywords is None:
                a.Keywords = []
            a.Keywords.append(Keyword(Text=v))

        elif (e == "AU"):  
            # (Primary) author/editor/translator,
            #  e.g. author, artist, created by, attribution, programmer,
            #  investigators, editor, director, interviewee, cartographer,
            #  composer, reporter, inventor, or institution.
            #  The tag must be repeated for each person. Synonym of A1.
            if a.Authors is None:
                a.Authors = []
            a.Authors.append(Author(FullName=v))
            # All
            # print(f"{e} -> {v}")
        elif (e == "A1"):  # Interviewee. (Primary) author. Synonym of AU.
            if a.Authors is None:
                a.Authors = []
            a.Authors.append(Author(FullName=v))
        elif (e == "A2"):  
            # Secondary author/editor/translator, e.g. editor, performers,
            #  sponsor, series editor, reporter, institution,
            #  name of file, producer, series director, department,
            #  interviewer, issuing organization, recipient, or narrator.
            #  The tag must be repeated for each person. Synonym of ED
            if a.Authors is None:
                a.Authors = []
            a.Authors.append(Author(FullName=v))
            # Not All
            # print(f"{e} -> {v}")
        elif (e == "ED"):  
            # Secondary author. Editor. Synonym of A2. Edition. 
            pass
            if a.Authors is None:
                a.Authors = []
            a.Authors.append(Author(FullName=v))
            # print(f"{e} -> {v}")
            # Downie, JS
            # Poursardar, F
            # Nichols, DM
            # Quaresma, P
        elif (e == "C1"):
            # Custom 1, e.g. legal note, cast, author affiliation,
            #  section, place published, time period, term, year cited,
            #  government body, contact name, scale, format of music,
            #  column, or sender's e-mail.
            pass
            if debug : print(f"{e} -> {v}")
            # in ACM
            #  C1 -> New York, NY, USA
        elif (e == "C2"):  
            # Custom 2, e.g. PMCID, credits, year published,
            #  unit of observation, date cited, congress number,
            #  contact address, area, form of composition,
            #  issue, issue date,
            #  recieipients e-mail, or report number.
            pass
            a.PMC = v
            # print(f"{e} -> {v}")
            # PMC10770784
            # PMC10618876
        elif (e == "C3"):  
            # Custom 3, e.g. size/length, title prefix, proceedings title,
            #  data type, PMCID, congress session, contact phone, size,
            #  music parts, or designated states.
            pass
            C3 = v
            # print(f"{e} -> {v}")
        elif e == "C5": 
            # Custom 5, e.g. format, packaging method, issue title,
            #  last update date, funding number, accompanying matter,
            #  format/length, references, or publisher.
            pass
            if debug: print(f"{e} -> {v}")
            # in EMBASE
            # C5 -> 15460689
        elif (e == "C6"):  # Custom 6, e.g. NIHMSID, CFDA number, legal status, issue, or volume.
            pass
            if debug: print(f"{e} -> {v}")
            # JAN 2024
            # OCT 2023
            # NIHMS1957582
            # EMS178744
        elif e == "C7":  # Custom 7, e.g. article number or PMCID.
            pass
            if debug : print(f"{e} -> {v}")
            # a.PMC = v # ?
            # 110170
            # 1333
            # 8847609
            # e94
            

        elif e == "DOI":  # Digital Object Identifier (DOI)
            a.DOI = v
        elif e == "DO":  # Digital Object Identifier (DOI).
            a.DOI = v
        elif e == "DI":  # Digital Object Identifier (DOI).
            a.DOI = v

        elif e == "LA":  # Language
            a.Language = v
            # if debug: print(f"{e} -> {v}")
            # eng, English, Chinese
        elif e == "ST":  # Short title or abbreviated case name
            pass
            if debug: print(f"{e} -> {v}")
            # Like TI if other language

        elif (e == "PY"):  
            # (Primary) (publication) year/date, e.g. year decided,
            #  year of conference, or year released.
            #  Must always use 4 digits, with leading zeros if before 1000.
            #  Synonym of Y1.
            a.Year = v
            # print(f"{e} -> {v}")   # All
            # 2012
            # 2023
        elif (e == "Y1"):
            # "Year///Date".[14] Primary date/year.
            #  Synonym of PY.
            # a.Year = v
            if debug: print(f"{e} -> {v}")
            
        elif e == "Y2":  
            # Access date or date enacted.
            #  Secondary date. Date of publication.
            # a.Year  = v
            # because usually have PY
            if debug: print(f"{e} -> {v}")
            # in GoogleScholar
            # Y2 -> 2025/07/17/02:15:28
        elif e == "YR":  # Publication year
            a.Year  = v

        elif (e == "DA"):  
            # Date, e.g. date accessed, last update date, date decided,
            #  date of collection, date released, deadline,
            #  date of code edition, or date enacted.
            pass
            # print(f"{e} -> {v}") # Not All
            # Oct, Dec, May 27, MAR, Feb
            if debug: print(f"{e} -> {v}")

        elif e == "SN":  # ISSN, ISBN, or report/document/patent number.
            a.SerialNumber = v
            # if debug: print(f"{e} -> {v}")
            # 16743415 (ISSN)
            # 1040-2446
            # 978-195591706-3 (ISBN)
            # 2212-1366 (Print)
            # 1099-4300 J9 - ENTROPY-SWITZ
            # 18761100 (ISSN); 978-981195537-2 (ISBN)


        elif e == "ER":  # End of reference. Must be the last tag.
            pass
            # print(f"{e} -> {v}")
            # /n
        elif e == "DP":  # Database provider.
            pass
            if v.__contains__("Google Scholar"):
                a.SourceBank = SourceBankType.GOOGLESCHOLAR
            # print(f"{e} -> {v}")
            # NLM
        elif e == "DB":  # Name of database.
            if v.__contains__("Scopus"):
                if a.SourceBank is None or a.SourceBank == SourceBankType.UNKNOWN:
                    a.SourceBank = SourceBankType.SCOPUS
            else:
                print(f"DB - Not Scopus is : {v}")
            # print(f"{e} -> {v}")
            # Scopus
        elif e == "AN":  # Accession number.
            pass
            if v.__contains__("WOS:"):
                # This is Web of Sciense
                a.SourceBank = SourceBankType.WOS
            else:
                if debug: print(f"{e} -> {v}")
            # WOS:000900130208031
            # 37847549

        elif (e == "AD"):  
            # (Author/editor/inventor) address, e.g. postal address,
            #  email address, phone number, and/or fax number. Institution.
            pass
            # All
            if debug: print(f"{e} -> {v}")
            # This is Affiliation
            # EnBW Kernkraft GmbH, Philippsburg, Germany
            # University of Colorado Anschutz Medical Campus School of Medicine, Aurora, CO, USA.
            # Computer Science, Georgia Institute of Technology, Atlanta, USA.
        elif (e == "M1"):
            # Number, publication number, text number, size, bill number,
            #  series volume, computer, issue, chapter, status,
            #  document number, start page, issue number,
            #  folio number, number of screens, application number,
            #  number of pages, public law number, or access date.
            #  Miscellaneous 1. A good place for type or genre information.
            pass
            if debug: print(f"{e} -> {v}")
            # in MBASE
            #  M1 -> (Barretto S.A.; Warren J.; Goodchild A.; Bird L.;
            #         Heard S.; Stumptner M.)
            #         Advanced Computing Research Centre,
            #         University of South Australia.
            #           but also have AD tag

        elif (e == "ID"):  
            # Reference identifier,
            #  may be limited to 20 alphanumeric characters.
            pass
            if debug: print(f"{e} -> {v}")
            # ?
        elif e == "IS":  # Number, e.g. issue or number of volumes.
            pass
            if debug: print(f"{e} -> {v}")
            # 18
            # 3
        elif (e == "PB"):  
            # Publisher, e.g. court, distributor, sponsoring agency,
            #  library/archive, assignee, institution, source,
            #  or university / degree grantor.
            pass
            if debug: print(f"{e} -> {v}")
            # Institute of Electrical and Electronics Engineers Inc.
            # Association for Computational Linguistics (ACL)
            # IEEE Computer Society
        elif e == "N1":  # Notes.
            pass
            if debug: print(f"{e} -> {v}")
            # Export Date: 10 February 2024; Cited By: 2;
            # Times Cited in Web of Science Core Collection: 0 Total Times Cited: 0 Cited Reference Count: 33
            # 2287-285x
            # Export Date: 10 February 2024; Cited By: 0; CODEN: ELKTA

            # Times Cited in Web of Science Core Collection: 24 Total Times Cited: 26 Cited Reference Count: 26
        elif (e == "SP"):  
            # Pages, description, code pages, number of pages,
            #  first/start page, or running time.
            pass
            if debug: print(f"{e} -> {v}")
            # 261-270
            # e50865
            # e94
            # e12-e22
            # 105219
            # 239
        elif (e == "T3"):  
            # source, title of show, section title, academic department,
            #  or full journal name.
            pass
            if debug: print(f"{e} -> {v}")
            # T3 -> SAC '08
            # T3 -> MIXHS '11
        elif (e == "VL"):  
            # Volume, code volume, access year, reporter volume, image size,
            #  edition, amount requested, rule number,
            #  volume/storage container, number, patent version number,
            #  code number, or degree.
            pass
            if debug: print(f"{e} -> {v}")
            # 2016-December
            # 52
            # 121
            # 5517 LNCS

        elif (e == "VO"): # Volume. Published Standard number
            pass
            if debug: print(f"{e} -> {v}")
            # in IEEE
            # VO -> 8
        elif (e == "VL"):
            # Volume, code volume, access year, reporter volume, image size,
            #  edition, amount requested, rule number,
            #  volume/storage container, number, patent version number,
            #  code number, or degree.
            pass
            if debug: print(f"{e} -> {v}")

        elif (e == "UR"):  
            # Web/URL. Can be repeated for multiple tags,
            #  or multiple URLs can be entered in the same tag
            #  as a semicolon-separated list.
            pass
            a.links = v
            # if debug: print(f"{e} -> {v}")
            # https://www.scopus.com/inward/record.uri?eid=2-s2.0-84961725690&doi=10.7667%2fPSPC151240&partnerID=40&md5=fa3bc7d65364213ec8ed9510f3a6da11
        elif (e == "LK"):  
            # Links
            #  Use in EMBASE but the UR is better
            # a.links = v
            if debug: print(f"{e} -> {v}")
        elif (e == "L1"):  
            # File attachments, e.g. figure. "Link to PDF.
            #  There is no practical length limit to this field.
            #  URL addresses can be entered individually,
            #  one per tag or multiple addresses can be entered on one line
            #  using a semi-colon as a separator. These links should end
            #  with a file name, and not simply a landing page.
            #  Use the UR tag for URL links." Internet link. Local file.
            # a.links = v
            # The same time have UR Tag
            if debug: print(f"{e} -> {v}")
            # in GoogleScholar
            #  L1 -> https://journals.sagepub.com/doi/pdf/10.1177/183335830803700104?casa_token=4yYaUfwFbAIAAAAA:NPfe_og_E28YaagfzvVGI91vlWW301gpVLRdXbw1s9bi_q__F8F0YvmMlFBExfXQi0CvU_bwD_Jz

        elif (e == "ET"):  
            # Edition, e.g. epub (electronic publication?) date,
            #  date published, session, action of higher court, version,
            #  requirement, description of material,
            #  international patent classification, or description.
            pass
            if debug: print(f"{e} -> {v}")
            # 2023/12/22
            # 2023/10/17
            # VOL. 1
            # PART 1
            # 9
        elif (e == "OP"):  
            #  Original publication, e.g. contents, history, content,
            #  version history, original grant number, or priority numbers.
            #  Other pages. Original foreign title.
            pass
            if debug: print(f"{e} -> {v}")

        elif (e == "SE"):  
            #  Section, screens, code section, message number, pages, chapter,
            #  filed date, number of pages, original release date, version,
            #  e-pub date, duration of grant, section number, start page,
            #  international patent number, or running time.
            pass
            if debug: print(f"{e} -> {v}")
        elif e == "EP":  # Pages. End page.
            pass
            if debug: print(f"{e} -> {v}")
            # 484
            # 400
        elif e == "PU":  # ?
            pass
            print(f"{e} -> {v}")
            # in WOS:
                # SPRINGER HEIDELBERG
                # W B SAUNDERS CO LTD
                # SPRINGER
                # in WOS
        elif e == "PI":  # ?
            pass
            print(f"{e} -> {v}")
            # PHILADELPHIA
            # EDINBURGH
            # COLLEGE PK
            # in WOS
        elif e == "PA":  # Personal notes.
            pass
            if debug: print(f"{e} -> {v}")
            # TWO COMMERCE SQ, 2001 MARKET ST, PHILADELPHIA, PA 19103 USA
            # CALEDONIAN EXCHANGE, 19A CANNING ST, EDINBURGH, Lothian, ENGLAND
            # GENTHINER STRASSE 13, D-10785 BERLIN, GERMANY
            # 130 QUEENS QUAY E, STE 1102, TORONTO, ON M5A 0P6, CANADA
        elif e == "J9":  # ?
            pass
            print(f"{e} -> {v}")
            # MEDICINE
            # J GLOB HEALTH
            # SEIZURE-EUR J EPILEP
            # CLIN CHEM LAB MED
            # in WOS
        elif e == "JI":
            pass
            print(f"{e} -> {v}")
            # JMIR Med. Inf.
            # Anal. Bioanal. Chem.
            # Medicine (Baltimore)
            # in WOS
        elif e == "WE":
            # In Web of Science (Clarivate) exports, WE often stands for Web of Science Edition.
            # It identifies which edition of the Web of Science the record belongs to, such as:
            #    - SCI – Science Citation Index
            #    - SSCI – Social Sciences Citation Index
            #    - AHCI – Arts & Humanities Citation Index
            #    - ESCI – Emerging Sources Citation Index
            pass
            print(f"{e} -> {v}")
            # Science Citation Index Expanded (SCI-EXPANDED)
            # Social Science Citation Index (SSCI)
            # Emerging Sources Citation Index (ESCI)
            # in WOS

        elif e == "CP":  # City/place of publication.[9][16] Issue.[21][18]
            pass
            # print(f"{e} -> {v}")
            # IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)
            # 16th ACM/IEEE International Conference on Human-Robot Interaction (HRI)
            # 9th Annual Sessions of the American-College-of-Surgeons (ACS)
            # in WOS
        elif (e == "A1"):  # Interviewee. (Primary) author. Synonym of AU.
            pass
            print(f"{e} -> {v}")
            # Assoc Computat Linguist
            # Assoc Advancement Artificial Intelligence
            # Assoc Comp Machinery
        elif e == "FU": # Funding source or funding acknowledgment.
            pass
            if debug: print(f"{e} -> {v}")
            # National Science Foundation
            # Projekt DEAL
            # i2b2 National Center for Biomedical Computing [U54LM008748]
            # The authors have no acknowledgements.
            # in WOS
            # FU -> Kamprad Family Foundation for Entrepreneurship, Research Charity; European Interreg project
        elif e == "FX":
            pass
            if debug: print(f"{e} -> {v}")
        elif e == "MA":
            pass
            if debug: print(f"{e} -> {v}")
            # LB1650
            # 1255P
            # S91
            # aqad150.27
            # 3076
        elif e == "U2": # Notes. User definable 2–5.
            pass
            if debug: print(f"{e} -> {v}")
            # in EMBASE
            # U2 -> L39466308
        elif e == "U4": # Notes. User definable 2–5.
            pass
            if debug: print(f"{e} -> {v}")
            # in EMBASE
            # U4 -> 2004-11-18

        else:
            pass
            if len(e) > 2:
                pass
            else:
                pass
                if e != "\n":
                    unknown_tag_list.append (e)
                    print(f"Unhandle Tag ....{e}")
                    print(f"    {e} -> {v}")
        # ------------------------------Parse all tag we need-----------------

    if a.Journal is None or a.Journal == "":
        a.Journal = C3  # I see in google scholar

    if a.SourceBank is None:
        a.SourceBank = sourcebanktype

    a.PublicationType =  ptype_list

    if debug:  print(f"List of unknown Tag of RIS : {unknown_tag_list}")
    return a


def import_ris_file(filepath, sourcebanktype=SourceBankType.UNKNOWN):
    # file: Union[TextIO, Path],

    #         with file.open(mode="r", newline=newline, encoding=encoding) as f:
    #             return parser(**kw).parse_lines(f)

    # Read file as list of lines
    with open(filepath, encoding="utf8") as file:
        lines = file.readlines()

    # parse lines into the RIS Block
    a_block = []
    import_article = 0
    tqdm = get_tqdm()
    bar = tqdm(total=len(lines), desc="Processing ")
    for i in range(0, len(lines) - 1):
        bar.update(1)
        a_block.append(lines[i])
        # Best Method for split block
        if lines[i][:5] == "ER  -":
            a = _parse_ris_block(a_block, sourcebanktype)
            r = PERSIST.insert_new_general_deduplicate_with_doi(a)
            
            if r is not None:
                import_article = import_article + 1
                bar.set_description(f"Processing - {import_article} article(s) imported ")

            a_block = []

        # # One Method for Split Block
        # if lines[i] == "\n":
        #     if lines[i+1] == "\n":
        #         parse_ris_block(a_block)
        #         a_block = []
    bar.close()
    logger.INFO(f"{import_article} article(s) imported")
