import sys
import click
from triplea.cli.main import cli
from triplea.service.repository.export.save_article import save_articlestr2json
import triplea.service.repository.persist as persist
from triplea.service.click_logger import logger


@cli.command("export_article", help="Export Article by identifier.")
@click.option(
    "--idtype",
    "-t",
    "identifier_type",
    type=click.Choice(
        [
            "pmid",
            "doi",
        ]
    ),
    multiple=False,
    required=True,
    help="""b""",
)
@click.option(
    "--id",
    "-d",
    "identifier",
    type=str,
    multiple=False,
    required=True,
    help="""a""",
)
@click.option(
    "--format",
    "-f",
    "format_type",
    type=click.Choice(["xml", "json", "csv"]),
    multiple=False,
    required=True,
    help="""Export article repository in specific format.
            xml : A simple csv file

            json :

                                """,
)
@click.option(
    "--output",
    "-o",
    "output_file",
    #   type=click.File('wb') ,
    type=str,
    multiple=False,
    required=True,
    help="File name & path of output graph format.",
)
def cli_export_article(identifier_type, identifier, format_type, output_file):
    if identifier_type == "pmid":
        a = persist.get_article_by_pmid(identifier)
        if a is None:
            logger.ERROR("Not found.")
            sys.exit(1)
            return

        a_title = a["Title"]
        a_journal = a["Journal"]
        a_doi = a["DOI"]
        a_pmid = a["PMID"]
        a_pmc = a["PMC"]
        a_state = a["State"]

        logger.INFO("")
        logger.INFO(f"Title   : {a_title}")
        logger.INFO(f"Journal : {a_journal}")
        logger.INFO(f"DOI     : {a_doi}")
        logger.INFO(f"PMID    : {a_pmid}")
        logger.INFO(f"PMC     : {a_pmc}")
        logger.INFO(f"State   : {a_state}")

        if "Authors" in a:
            if a["Authors"] is not None:
                authors = ""
                for author in a["Authors"]:
                    authors = authors + author["FullName"] + ", "
                logger.INFO(f"Authors : {authors}")

        if "Keywords" in a:
            if a["Keywords"] is not None:
                keywords = ""
                for k in a["Keywords"]:
                    keywords = keywords + k["Text"] + ", "
                logger.INFO(f"Keywords: {keywords}")

        if format_type == "json":
            save_articlestr2json(a, output_file)

    elif identifier_type == "pmcid":
        raise NotImplementedError
    elif identifier_type == "doi":
        raise NotImplementedError
        sys.exit(1)

    sys.exit(0)
