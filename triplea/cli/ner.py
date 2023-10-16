from string import printable
import click

# from triplea.service.nlp.ner import get_title_ner  # Expire Module
from triplea.service.click_logger import logger
from triplea.cli.main import cli


@cli.command("ner", help="Single NER with custom model.")
@click.option("--title", prompt="Article Title", help="The person to greet.")
def ner_title(title):
    logger.INFO("NER this Title base on custom mode for extracting major topic:")
    logger.INFO(title)
    try:
        # ner = get_title_ner(title)  # Expire Module
        ner = ""
    except Exception:
        logger.ERROR("Error")
        raise
    for e in ner:
        logger.INFO(f"{e.label_} : {e.ents}")

    click.echo("Continue? [y/n] ", nl=False)
    c = click.getchar()
    click.echo()
    if c == "y":
        logger.INFO("We will go on")
        ner_title()
    elif c == "n":
        pass
    else:
        logger.WARNING("Invalid input :(")
        logger.WARNING(
            'You pressed: "'
            + "".join(["\\" + hex(ord(i))[1:] if i not in printable else i for i in c])
            + '"'
        )


if __name__ == "__main__":
    pass
    ner_title()
