import sys
import click
from triplea.cli.main import cli
import triplea.service.repository.export as repo_export
from triplea.service.click_logger import logger


@cli.command("export_llm", help="Export preTrain LLM.")
@click.argument(
    "output_directory",
    type=str,
    required=True,
    metavar="OUTPUT_DIRECTORY",
    # help="Directory path of output.",
)
@click.option(
    "--merge",
    "-m",
    "merge",
    type=bool,
    multiple=False,
    required=False,
    default=False,
    help="Merge alldata in one file.",
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
    help="Specify the maximum number of samples to export. Set to 0 for no limit.",
)
def export_llm(output_directory, merge, proccess_bar, limit_sample):
    """
    Export preTrain LLM.

    Args:
        output_directory (str): Directory path of output.
        merge (bool): Merge alldata in one file.
        proccess_bar (bool): Run proccess bar in command line.
        limit_sample (int):
        Specify the maximum number of samples to export. Set to 0 for no limit.

    Returns:
        str: "Export successful" if export is successful.

    Raises:
        Exception: If export fails.
    """
    try:
        repo_export.export_pretrain_llm_in_dir(
            output_directory, merge, proccess_bar, limit_sample
        )
        sys.exit(0)
    except Exception as e:
        logger.ERROR("Error: {}".format(str(e)))
        sys.exit(1)
