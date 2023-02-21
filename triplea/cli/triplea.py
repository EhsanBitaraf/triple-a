import click
from triplea.service.nlp.ner import get_title_ner
from triplea.service.click_logger import logger

@click.command()
@click.option("--br", is_flag=True, show_default=True, default=True, help="Add a thematic break")
def main():
