import click
from triplea.service.repository.general import move_state_forward
from triplea.service.click_logger import logger
from triplea.service.repository.persist import refresh

@click.command()
@click.option("--state", prompt="Current State", help="Current state for start to move next state.")
def next(state:int):
    try:
        state = int(state)
    except:
        logger.ERROR(f'State {state} Value Error.')
        return


    logger.INFO(f'Read Current State {state} ...', forecolore='cyan')
    next_state = state + 1
    if next_state == 1:
        logger.INFO(f'Next State {next_state} for get detail information of article ...')
    elif next_state == 2:
        logger.INFO(f'Next State {next_state} for extract graph ...')
    elif next_state == 3:
        logger.INFO(f'Next State {next_state} for get Citation ...')
    else:
        logger.WARNING(f'Next State {next_state} for  ...')

    move_state_forward(state)
    refresh()




if __name__ == '__main__':
    pass
    next()