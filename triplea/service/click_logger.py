import click
from typing import Optional


class Log:
    def _prep(self, message: str, deep: Optional[int] = 0) -> str:
        PREFIX_CHAR = " "
        prefix = ""
        if deep > 0:
            for i in range(1, deep):
                prefix = prefix + PREFIX_CHAR
            message = prefix + message

        else:
            pass

        return message

    def DEBUG(
        self,
        message: str,
        forecolore: Optional[str] = "green",
        deep: Optional[int] = 0,
    ):
        click.secho(self._prep(message, deep=deep), fg=forecolore)

    def INFO(
        self,
        message: str,
        forecolore: Optional[str] = "green",
        deep: Optional[int] = 0,
    ):
        click.secho(self._prep(message, deep=deep), fg=forecolore)

    def WARNING(
        self,
        message: str,
        forecolore: Optional[str] = "yellow",
        deep: Optional[int] = 0,
    ):
        click.secho(self._prep(message, deep=deep), fg=forecolore)

    def ERROR(
        self,
        message: str,
        forecolore: Optional[str] = "red",
        deep: Optional[int] = 0,
    ):
        click.secho(self._prep(message, deep=deep), fg=forecolore)

    def CRITICAL(
        self,
        message: str,
        forecolore: Optional[str] = "red",
        deep: Optional[int] = 0,
    ):
        click.secho(self._prep(message, deep=deep), fg=forecolore)


logger = Log()


if __name__ == "__main__":
    logger.DEBUG("DEBUG is 10")
    logger.INFO("INFO is 20")
    logger.WARNING("WARNING is 30")
    logger.ERROR("ERROR is 40")
    logger.ERROR("CRITICAL is 50")
