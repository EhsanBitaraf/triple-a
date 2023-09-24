import click
from triplea.service.click_logger import logger
from triplea.cli.main import cli
import triplea.service.repository.import_file as imp


@cli.command(
    "import",
    help="""import article from specific file format
              to article repository.""",
)
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--type",
    "-t",
    "import_type",
    type=click.Choice(
        [
            "rayyan",
            "triplea",
        ]
    ),
    multiple=False,
    required=True,
    help="""import article from specific file format to article repository.
            The type of input file format can be different. These include:

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
    help="""Import article repository in specific format.
                                csv :

                                json :

                                """,
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
def import_file(filename, import_type, format_type, proccess_bar):
    logger.INFO(
        """import article from specific file format
    to article repository."""
    )
    if import_type == "triplea":
        if format_type == "json":
            imp.import_triplea_json(filename, proccess_bar)

        elif format_type == "csv":
            raise NotImplementedError
        else:
            logger.ERROR("Invalid Format.")

    elif import_type == "rayyan":
        raise NotImplementedError
    else:
        logger.ERROR("Invalid Type.")
