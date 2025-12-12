
"""
Version: 0.0.1
Status: Flagship

- Move to TripleA 2025-07-20
- Update clean_publication_type


Usage:
read_dataset_for_analysis
    clean_language_dataset
    clean_publication_type
    clean_year
    normalized_issn
    scimago_data_enrichment
conver_df_to_csv
    detect_field_types
create_table
"""

# from src.config import DATASET_FILE, DATA_DIR, ROOT
import json
import os
import re
import pandas as pd
from pathlib import Path
from triplea.config.settings import ROOT
import csv


def clean_authors(d):
    """
    Ensure all author names in d['authors'] end with a period.
    Example:
        {"authors": ["Abidi, S", "Bray, B.E", "Alegre, E."]}
        => {"authors": ["Abidi, S.", "Bray, B.E.", "Alegre, E."]}
    """
    if "authors" not in d or not isinstance(d["authors"], list):
        return d  # در صورت نبودن کلید authors یا اشتباه بودن نوع داده، تغییری نده

    cleaned = []
    for a in d["authors"]:
        if not isinstance(a, str):
            cleaned.append(a)
            continue

        a = a.strip()
        if not a.endswith("."):
            a += "."
        cleaned.append(a)

    d["authors"] = cleaned
    return d


def clean_language_dataset(d):
    # ---- Clean Language------
    lg = d['language']
    if lg in ['eng','en']:
        d['language'] = 'English'
    elif lg in ['chi','Chinese']:
        d['language'] = 'Chinese'
    elif lg in ['fre','French']:
        d['language'] = 'French'
    elif lg in ['ger','German']:
        d['language'] = 'German'

    # ---- Clean Language------

def clean_publication_type(d):
   # ---- Clean publication_type
    if isinstance( d['publication_type'],list):
        # print(d['publication_type'])
        pts = d['publication_type']
    else:
        pt = d['publication_type']
        if pt is not None:
            pts = pt.split(",")
        else:
            pts = []
    
    clean_publication_type = []
    for p in pts:
        p = p.strip()
        if p in ['Review',
                 'Systematic Review',
                 "Scoping Review",
                 'Meta-Analysis',]:
            p = 'Review'
        elif p == '':
            p = None
        elif p in ['Journal Article','Historical Article','JOUR', 'Article']:
            p = 'Journal Article'
        elif p in ['Randomized Controlled Trial',
                   'Clinical Trial Protocol',
                   'Clinical Trial',
                   'Controlled Clinical Trial',
                   'English Abstract',
                   'Comparative Study',
                   'Multicenter Study',
                   'Observational Study',
                   'Validation Study',
                   'Research Support',
                    "Clinical Trial, Phase I",
                    "Clinical Trial, Phase I",
                    "Clinical Trial, Phase II",
                    "Clinical Trial, Veterinary",
                    "Research Support, U.S. Gov't, Non-P.H.S.",
                    "Research Support, N.I.H., Intramural",
                    "Research Support, Non-U.S. Gov't",
                    "Research Support, U.S. Gov't, P.H.S.",
                    "Research Support, N.I.H., Extramural",
                   "Non-U.S. Gov't",
                   "U.S. Gov't",
                   "Intramural",
                   'Extramural',
                   "Twin Study"
                   ]:
            p = 'Journal Article'

        elif p in ['N.I.H.','Non-P.H.S.', 'P.H.S.']:
            p = 'Journal Article'

        elif p in ['CONF',
                   'CPAPER', # WOS
                   'Conference paper',
                   'Conference Paper',
                   'Conference Abstract',
                     ]:
            p = 'Conference Article'

        elif p in ['BOOK','CHAP', 'THES', 'Book chapter', 'Book'
                   ]:
            p = 'Book'

        elif p in ['Published Erratum', 'Erratum']:
            p = 'Published Erratum'


        elif p in ['Preprint','GEN']:
            p = 'Preprint'
        elif p in ['Editorial']:
            p = 'Editorial'

        elif p in ['RPRT']:
            p = 'Report'
        elif p in ['ELEC']:
            p = 'Electronic'

        elif p in ['Comment']:
            p = 'Comment'
        elif p in ['Letter']:
            p = 'Letter'

        elif p in ['Conference review', 'Conference Review']:
            p = 'Conference review'
        elif p in ['PhD Thesis']:
            p = 'PhD Thesis'


        elif p in ["Veterinary"]:
            p = "Veterinary"

        elif p in ["Video-Audio Media"]: # PubMed
            p = "Video-Audio Media"

        elif p in ["Clinical Study"]: # PubMed
            p = "Clinical Study"

        elif p in ["Case Reports"]: # PubMed
            p = "Case Reports"

        elif p in ["Evaluation Study"]: # PubMed
            p = "Evaluation Study"

        elif p in ["Dataset"]: # PubMed
            p = "Dataset"

        elif p in ["Retracted Publication",# PubMed
                    "Retracted" # Scoupus
                    ]: # Scoupus
            p = "Retracted Publication"

        else:
            p = f"{p} (Unknown)"
            # print(f"clean_publication_type -> {p}")

        if p is not None:
            clean_publication_type.append(p)

    my_set = set(clean_publication_type)
    list(my_set)
    d['publication_type'] = list(my_set)
    # ---- Clean publication_type

def clean_year(d):
    # ---- Clean Year------
    y = d['year']
    try:
        y_n = int(y)
    except: # invalid literal for int() with base 10: '2022 Nov-Dec 23'
        if len(y) !=4:
            d['year'] = y[:4]
        else:
            print(f"clean_year -> {y}")
    # ---- Clean Year------

def normalized_issn(issn):
    """
    Normalizes the ISSN field by splitting it on the comma and returning a list of ISSNs.
    """
    issn_list = []
    if issn.__contains__(','):
        pass
        l = issn.split(',')
        for i in l:
            i= i.strip()
            if len(i) == 8 :
                i = i[:4] + '-' + i[-4:]
                issn_list.append(i)
            else:
                print(i)
    else:
        issn = issn.strip()
        issn = issn[:4] + '-' + issn[-4:]
        issn_list.append(issn)
    return issn_list

def normalize_issn(journal_issn: str) -> str:
    """
    This function for my dataset
    """
    # Match ISSN patterns: with or without hyphen, and check digit can be X
    issn_pattern = re.compile(r'\b(\d{4})-?(\d{3}[0-9Xx])\b(?:\s*\(ISSN\))?')

    matches = issn_pattern.findall(journal_issn)
    if matches:
        # Format the first ISSN found correctly as XXXX-XXXX
        prefix, suffix = matches[0]
        return f"{prefix}-{suffix.upper()}"

    # No ISSN found, return the original string
    return journal_issn


def scimago_data_enrichment(df, scimagojr_csv_file_path):
    # scimagojr_csv_file_path = DATA_DIR / 'scimagojr 2023.csv'
    scimago_df = pd.read_csv(scimagojr_csv_file_path,
                            delimiter=";",
                            # encoding='latin-1',
                            # encoding='utf-8'
                            )

    scimago_df['normal_issn'] = scimago_df['Issn'].apply(normalized_issn)

    # Explode the DataFrame to create new rows for each ISSN
    final_scimago_df = scimago_df.explode('normal_issn')

    # This file use for qlickview
    DATA_DIR = Path(os.path.dirname(scimagojr_csv_file_path))
    final_scimago_df.to_csv(DATA_DIR / 'scimagojr 2023_normal_issn.csv',)

    final_scimago_df = final_scimago_df.drop(columns=["H index", "Sourceid" ,"Type", "Issn",
                                        "SJR",
                                        "Total Docs. (2023)",
                                        "Total Docs. (3years)",
                                        "Total Refs.",
                                        "Total Cites (3years)",
                                        "Citable Docs. (3years)",
                                        "Cites / Doc. (2years)",
                                        "Ref. / Doc.",
                                        "%Female",
                                        "Overton",
                                        "SDG",
                                        "Coverage",
                                        "Categories",
                                        "Areas"  
                                        ]
                                        )

    new_df = final_scimago_df.groupby(list(final_scimago_df.columns)).size().reset_index(name='Document_Count')
    new_df = new_df.rename(columns={'Rank': 'journal_rank'})
    new_df = new_df.rename(columns={'Title': 'journal_title'})
    new_df = new_df.rename(columns={'SJR Best Quartile': 'journal_q'})
    new_df = new_df.rename(columns={'Country': 'journal_country'})
    new_df = new_df.rename(columns={'Region': 'journal_region'})
    new_df = new_df.rename(columns={'Publisher': 'journal_publisher'})
    new_df = new_df.drop(columns=[ "Document_Count"])


    df = pd.merge(df, new_df, left_on='journal_issn', right_on='normal_issn', how='left')

    return df


def _smart_title_case(text):
    # Only apply title-case rules if the text is fully uppercase
    if not isinstance(text, str):
        return text
    if text != text.upper():
        return text  # Return original text if it is not full uppercase
    
    # Words to keep lowercase unless they are the first word
    lower_words = {"of", "the", "and", "in", "on", "at", "for", "to"}

    words = text.strip().split()
    if not words:
        return text

    # First word capitalized
    result = [words[0].capitalize()]

    # Process remaining words
    for w in words[1:]:
        if w.lower() in lower_words:
            result.append(w.lower())
        else:
            result.append(w.capitalize())

    return " ".join(result)

def fill_unmapped_journall_with_publisher(df):
    # Make a copy to avoid modifying the original dataframe
    df = df.copy()

    # Identify rows with empty or NaN journal_title
    mask = df['journal_title'].isna() | (df['journal_title'].astype(str).str.strip() == "")

    # Fill journal_title using smart title case applied to publisher
    df.loc[mask, 'journal_title'] = (
        df.loc[mask, 'publisher']
        .astype(str)
        .apply(_smart_title_case)
    )

    return df

def read_dataset_for_analysis(DATASET_FILE, scimagojr_csv_file_path):
    scimagojr_csv_file_path = Path(scimagojr_csv_file_path)
    with open(DATASET_FILE, "r") as json_file:
        data = json.load(json_file)

    for d in data:
        clean_language_dataset(d)
        clean_publication_type(d)
        clean_year(d)
        clean_authors(d)
        d['journal_issn'] = normalize_issn(d['journal_issn'])

    # data = read_repository(DATASET_FILE)
    df = pd.DataFrame(data)

    df = scimago_data_enrichment(df, scimagojr_csv_file_path)

    # After map fill unmapped
    df = fill_unmapped_journall_with_publisher(df)
    return df

def detect_field_types(df):
    main_fields = []
    one_to_many_fields = []

    for column in df.columns:
        if df[column].apply(lambda x: isinstance(x, list)).all():
            one_to_many_fields.append(column)
        else:
            main_fields.append(column)

    return main_fields, one_to_many_fields

def conver_df_to_csv(df, output_dir = ROOT):
    # Make sure output_dir is a Path object
    output_dir = Path(output_dir)

    # Create the directory if it does not exist, including parents
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Output directory is : {output_dir}")

    main_fields, one_to_many_fields = detect_field_types(df)
    df = df.reset_index(drop=True)

    print("These are is main fields:")
    print(main_fields)

    print("These are one to many fields:")
    print(one_to_many_fields)

    # Create main CSV with explicit ID column
    main_df = df[main_fields].copy()
    main_df.insert(0, 'id', main_df.index)
    # main_df.to_csv(output_dir / 'main.csv', index=False)
    main_df.to_csv(output_dir / 'main.csv', index=False, quoting=csv.QUOTE_ALL, escapechar='\\')

    print("-- main.csv saved.")

    # Create separate CSV files for one-to-many fields
    for field in one_to_many_fields:
        rows = []
        for index, row in df.iterrows():
            for item in row[field]:
                rows.append({'id': index, field: item})
        output_file = output_dir / f'main_{field}.csv'
        pd.DataFrame(rows).to_csv(output_file, index=False)
        print(f"-- main_{field}.csv saved.")
