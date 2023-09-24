import click
from triplea.service.repository.pipeline_core import move_state_forward
from triplea.service.click_logger import logger
from triplea.service.repository.persist import refresh
from triplea.cli.main import cli


@cli.command(
    "next",
    help="""Moves the articles state in the Arepo from the current state
    to the next state.""",
)
@click.option(
    "--state",
    "-s",
    "current_state",
    prompt="Current State",
    help="Current state for start to move next state.",
)
def next(current_state: int):
    try:
        current_state = int(current_state)
    except Exception:
        logger.ERROR(f"State {current_state} Value Error.")
        return

    logger.INFO(f"Read Current State {current_state} ...", forecolore="cyan")
    next_state = current_state + 1
    if next_state == 1:
        logger.INFO(
            f"""Next State {next_state} for get detail information
            of article ..."""
        )
    elif next_state == 2:
        logger.INFO(f"Next State {next_state} for parse details info ...")
    elif next_state == 3:
        logger.INFO(f"Next State {next_state} for get Citation ...")
    else:
        logger.WARNING(f"Next State {next_state} for  ...")

    move_state_forward(current_state)
    refresh()


if __name__ == "__main__":
    pass
    next()
