from triplea.cli.main import cli
import click
import os
from triplea.config.settings import ENV_PATH_FILE
from triplea.service.click_logger import logger


@cli.command("config", help="Configuration additional setting. ")
@click.option(
    "--command",
    "-c",
    "command",
    type=click.Choice(["info", "update"]),
    multiple=False,
    required=False,
    help="""Configuration Command :

                    info : Get environment variable

                    update : Set new environment variable

                    """,
)
def configuration(command):
    if command == "info":
        print(ENV_PATH_FILE)
        if os.path.isfile(ENV_PATH_FILE):
            logger.INFO("Env file is exist.")
        else:
            logger.INFO("Env file is not exist.")

        # print all environment variable
        for name, value in os.environ.items():
            print("     {0}: {1}".format(name, value))
    elif command == "update":
        TRIPLEA_DB_TYPE = click.prompt("TRIPLEA_DB_TYPE", default="TinyDB")
        if TRIPLEA_DB_TYPE == "MongoDB":
            AAA_MONGODB_CONNECTION_URL = click.prompt(
                "AAA_MONGODB_CONNECTION_URL",
                default="mongodb://user:pass@127.0.0.1:27017/",
            )
            AAA_MONGODB_DB_NAME = click.prompt(
                "AAA_MONGODB_DB_NAME", default="articledata"
            )
        elif TRIPLEA_DB_TYPE == "TinyDB":
            AAA_TINYDB_FILENAME = click.prompt(
                "AAA_TINYDB_FILENAME", default="articledata.json"
            )

        else:
            raise NotImplementedError

        AAA_TPS_LIMIT = click.prompt("AAA_TPS_LIMIT", default=1, type=int)
        AAA_PROXY_HTTP = click.prompt("AAA_PROXY_HTTP", default="")
        AAA_PROXY_HTTPS = click.prompt("AAA_PROXY_HTTPS", default="")
        AAA_REFF_CRAWLER_DEEP = click.prompt(
            "AAA_REFF_CRAWLER_DEEP", default=1, type=int
        )
        AAA_CITED_CRAWLER_DEEP = click.prompt(
            "AAA_CITED_CRAWLER_DEEP", default=1, type=int
        )

        logger.WARNING("The settings will change as follows: ")
        logger.WARNING(f"   TRIPLEA_DB_TYPE:{TRIPLEA_DB_TYPE} ")
        if TRIPLEA_DB_TYPE == "MongoDB":
            logger.WARNING(
                f"   AAA_MONGODB_CONNECTION_URL: {AAA_MONGODB_CONNECTION_URL} "
            )
            logger.WARNING(f"   AAA_MONGODB_DB_NAME: {AAA_MONGODB_DB_NAME} ")
        elif TRIPLEA_DB_TYPE == "TinyDB":
            logger.WARNING(f"   AAA_TINYDB_FILENAME: {AAA_TINYDB_FILENAME} ")

        logger.WARNING(f"   AAA_TPS_LIMIT: {AAA_TPS_LIMIT} ")
        logger.WARNING(f"   AAA_PROXY_HTTP: {AAA_PROXY_HTTP} ")
        logger.WARNING(f"   AAA_PROXY_HTTPS: {AAA_PROXY_HTTPS} ")
        logger.WARNING(f"   AAA_REFF_CRAWLER_DEEP: {AAA_REFF_CRAWLER_DEEP} ")
        logger.WARNING(f"   AAA_CITED_CRAWLER_DEEP: {AAA_CITED_CRAWLER_DEEP} ")

        if click.confirm("Do you want to continue?"):
            with open(ENV_PATH_FILE, "w") as file:
                file.writelines(f"TRIPLEA_DB_TYPE={TRIPLEA_DB_TYPE} \n")
                if TRIPLEA_DB_TYPE == "MongoDB":
                    file.writelines(
                        f"""AAA_MONGODB_CONNECTION_URL=
                        {AAA_MONGODB_CONNECTION_URL} \n"""
                    )
                    file.writelines(
                        f"""AAA_MONGODB_DB_NAME=
                                    {AAA_MONGODB_DB_NAME} \n"""
                    )
                elif TRIPLEA_DB_TYPE == "TinyDB":
                    file.writelines(
                        f"""AAA_TINYDB_FILENAME=
                                    {AAA_TINYDB_FILENAME} \n"""
                    )

                file.writelines(f"AAA_TPS_LIMIT={AAA_TPS_LIMIT} \n")
                file.writelines(f"AAA_PROXY_HTTP={AAA_PROXY_HTTP} \n")
                file.writelines(f"AAA_PROXY_HTTPS={AAA_PROXY_HTTPS} \n")
                file.writelines(
                    f"""AAA_REFF_CRAWLER_DEEP=
                                {AAA_REFF_CRAWLER_DEEP} \n"""
                )
                file.writelines(
                    f"""AAA_CITED_CRAWLER_DEEP=
                                {AAA_CITED_CRAWLER_DEEP} \n"""
                )

    else:
        raise NotImplementedError
