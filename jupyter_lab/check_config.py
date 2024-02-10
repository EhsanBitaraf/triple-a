import os
from triplea.config.settings import ENV_PATH_FILE
from triplea.config.settings import SETTINGS
from triplea.service.click_logger import logger


if __name__ == "__main__":
    if os.path.isfile(ENV_PATH_FILE):
        logger.INFO("Env file is exist.")
    else:
        logger.INFO("Env file is not exist.")

    logger.WARNING(f"   TRIPLEA_DB_TYPE:{SETTINGS.AAA_DB_TYPE} ")
    if SETTINGS.AAA_DB_TYPE == "MongoDB":
        logger.WARNING(
            f"   AAA_MONGODB_CONNECTION_URL: {SETTINGS.AAA_MONGODB_CONNECTION_URL} "
        )
        logger.WARNING(f"   AAA_MONGODB_DB_NAME: {SETTINGS.AAA_MONGODB_DB_NAME} ")
    elif SETTINGS.AAA_DB_TYPE == "TinyDB":
        logger.WARNING(f"   AAA_TINYDB_FILENAME: {SETTINGS.AAA_TINYDB_FILENAME} ")