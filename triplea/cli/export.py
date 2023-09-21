import json
import click
from triplea.cli.main import cli
import triplea.service.graph.extract as gextract
import triplea.service.graph.export as gexport
import triplea.service.repository.export as repo_export
from triplea.service.click_logger import logger


@cli.command("export", help="Export article repository in specific format.")
@click.option(
    "--type",
    "-t",
    "export_type",
    type=click.Choice(
        [
            "rayyan",
            "triplea",
        ]
    ),
    multiple=False,
    required=True,
    help="""Export article in article repository 
                                The type of output file format can be different. These include:

                                rayyan : 

                                triplea : 

                                """,
)
@click.option(
    "--format",
    "-f",
    "format_type",
    type=click.Choice(["csv", "json"]),
    multiple=False,
    required=True,
    help="""Export article repository in specific format.
                                csv : 

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
    help="File name & path of output file format.",
)
@click.option(
    "--bar",
    "-b",
    "proccess_bar",
    type=bool,
    multiple=False,
    required=False,
    default=True,
    help="Run proccess bar in command line.",
)
def export(export_type, format_type, output_file, proccess_bar):
    if export_type == "triplea":
        if format_type=="csv":
            raise NotImplementedError
        elif format_type=="json":
            json_str = repo_export.export_triplea_json()
            with open(output_file, "w", encoding="utf-8") as file1:
                file1.write(json_str)
        else:
            logger.ERROR("Invalid Format.")

    elif export_type == "rayyan":
        if format_type=="csv":
            csv = repo_export.export_rayyan_csv()
            with open(output_file, "w", encoding="utf-8") as file1:
                file1.write(csv)
        else:
            logger.ERROR("Invalid Format.")



    else:
        logger.ERROR(f"Invalid value for '--type' / '-t': {export_type}")
