import json
import click
from triplea.cli.main import cli
import triplea.service.repository.persist as persist
from triplea.service.click_logger import logger


@cli.command("arepo", help="Access Article Repository.")
@click.option(
    "--command",
    "-c",
    "command",
    type=click.Choice(["info", "convert", "sdd"]),
    multiple=False,
    required=False,
    help="""Access Article Repository Command :

                    info :

                    convert :

                    """,
)
@click.option(
    "--pubmedid",
    "-pmid",
    "pmid",
    type=str,
    multiple=False,
    required=False,
    help="get PMID and return Article Data.",
)
@click.option(
    "--output",
    "-o",
    "output",
    type=str,
    multiple=False,
    required=False,
    help="save output to file.",
)
def arepo(command, pmid, output):
    if command == "info":
        logger.INFO(
            "Number of article in article repository is "
            + str(persist.get_all_article_count())
        )
        logger.INFO(f"{persist.get_all_node_count()} Node(s) in article repository.")
        logger.INFO(f"{persist.get_all_edge_count()} Edge(s) in article repository.")
        data = persist.get_article_group_by_state()
        for i in range(-3, 7):
            w = 0
            for s in data:
                if s["State"] == i:
                    w = 1
                    n = s["n"]
                    if n != 0:
                        logger.INFO(f"{n} article(s) in state {i}.")
            if w == 0:
                pass
                # logger.INFO(f'0 article(s) in state {i}.')
    elif command == "convert":
        raise NotImplementedError
    elif command is None:
        pass
    else:
        logger.ERROR(f"Invalid value for '--command' / '-c': {command}")

    if pmid is not None:
        a = persist.get_article_by_pmid(pmid)
        if a is None:
            logger.ERROR("Not found.")
            return

        output_data = a
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

    if output is not None:
        data = json.dumps(output_data, indent=4)
        with open(output, "w") as outfile:
            outfile.write(data)
            outfile.close()