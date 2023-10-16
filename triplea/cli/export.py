import sys
import click
from triplea.cli.main import cli
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
    type=click.Choice(["csv", "json", "csvs"]),
    multiple=False,
    required=True,
    help="""Export article repository in specific format.
            csv : A simple csv file

            json :

            csvs : Several csv files are created
            and one-to-many relationships
            are maintained in them

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
    default=False,
    help="Run proccess bar in command line.",
)
@click.option(
    "--limit",
    "-l",
    "limit_sample",
    type=int,
    multiple=False,
    required=False,
    default=0,
    help=".",
)
def export(export_type, format_type, output_file, proccess_bar, limit_sample):
    """
    Export articles from a repository in a specific format.

    Args:
        export_type (str):
        Specifies the type of export, either "triplea" or "rayyan".
        format_type (str):
        Specifies the format of the exported file, either "csv" or "json".
        output_file (str):
        Specifies the name and path of the output file.
        proccess_bar (bool):
        Specifies whether to display a progress bar during the export process.

    Raises:
        NotImplementedError:
        If the format type is "csv" and the export type is "triplea".

    Returns:
        None
    """
    if export_type == "triplea":
        if format_type == "csv":
            csv = repo_export.export_triplea_csv(proccess_bar, limit_sample)
            with open(output_file, "w", encoding="utf-8") as file1:
                file1.write(csv)
        elif format_type == "csvs":
            repo_export.export_triplea_csvs_in_relational_mode_save_file(
                output_file, proccess_bar, limit_sample
            )
        elif format_type == "json":
            json_str = repo_export.export_triplea_json(proccess_bar, limit_sample)
            with open(output_file, "w", encoding="utf-8") as file1:
                file1.write(json_str)
        else:
            logger.ERROR("Invalid Format.")
            sys.exit(1)

    elif export_type == "rayyan":
        if format_type == "csv":
            csv = repo_export.export_rayyan_csv()
            with open(output_file, "w", encoding="utf-8") as file1:
                file1.write(csv)
        else:
            logger.ERROR("Invalid Format.")
            sys.exit(1)

    else:
        logger.ERROR(f"Invalid value for '--type' / '-t': {export_type}")
        sys.exit(1)

    sys.exit(0)
