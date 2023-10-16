import json
import click
import triplea.service.repository.persist as persist
from triplea.service.click_logger import logger


def import_triplea_json(filename, proccess_bar=False):
    """
    Imports data from a JSON file and creates articles in a repository using the imported data.

    Args:
        filename (str): The name of the JSON file to import.
        proccess_bar (bool, optional): Whether to display a progress bar during the import process. Defaults to True.

    Returns:
        None

    Example Usage:
        import_triplea_json('data.json', proccess_bar=True)
    """
    # Opening JSON file
    with open(filename) as f:
        data = json.load(f)
    logger.INFO(f"{len(data)} articles have been entered.")
    if proccess_bar:
        bar = click.progressbar(length=len(data), show_pos=True, show_percent=True)

    for a in data:
        persist.create_article(a)
        if proccess_bar:
            bar.label = "Article " + a["PMID"] + " write in article repo. "
            bar.update(1)
    print()
    persist.refresh()
    logger.INFO("Import Complete.")
