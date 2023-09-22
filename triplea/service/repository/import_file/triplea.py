
import json
import click
# from triplea.service.repository.persist import create_article
# import triplea.service.repository.persist as persist

from persist import create_article




def import_triplea_json(filename, proccess_bar=True):
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
    print(type(data))
    if proccess_bar:
        bar = click.progressbar(length=len(data), show_pos=True, show_percent=True)

    for a in data:
        create_article(a)
        if proccess_bar:
            bar.label = (
                "Article "
                + a['PMID']
                + " write in article repo. "
            )
            bar.update(1)


if __name__ == "__main__":
    import_triplea_json(r"C:\Users\Bitaraf\Desktop\ff\BibliometricAnalysis.json")
    
