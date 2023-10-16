import os
import pathlib
from typing import Optional
from pydantic import BaseSettings
from dotenv import load_dotenv
import tomli

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent
DB_ROOT_PATH = ROOT.parent / "database"
ENV_PATH_FILE = ROOT / "config" / "environment_variable" / ".env"

load_dotenv(ENV_PATH_FILE, override=True)

with open("pyproject.toml", "rb") as f:
    pyproject = tomli.load(f)
    version = pyproject["tool"]["poetry"]["version"]


class Settings(BaseSettings):
    # ---------------My Envirement Varable-------------------------------
    AAA_DB_TYPE: Optional[str] = os.getenv("TRIPLEA_DB_TYPE", "TinyDB")
    AAA_TINYDB_FILENAME: Optional[str] = os.getenv(
        "AAA_TINYDB_FILENAME", "default-tiny-db.json"
    )
    AAA_MONGODB_CONNECTION_URL: Optional[str] = os.getenv(
        "AAA_MONGODB_CONNECTION_URL", "mongodb://user:pass@127.0.0.1:27017/"
    )
    AAA_MONGODB_DB_NAME: Optional[str] = os.getenv(
        "AAA_MONGODB_DB_NAME", "default-aaa-mongo-db"
    )
    AAA_TPS_LIMIT: Optional[int] = os.getenv("AAA_TPS_LIMIT", 1)
    AAA_PROXY_HTTP: Optional[str] = os.getenv("AAA_PROXY_HTTP", "")
    AAA_PROXY_HTTPS: Optional[str] = os.getenv("AAA_PROXY_HTTPS", "")
    AAA_REFF_CRAWLER_DEEP: Optional[int] = os.getenv("AAA_REFF_CRAWLER_DEEP", 1)
    AAA_CITED_CRAWLER_DEEP: Optional[int] = os.getenv("AAA_CITED_CRAWLER_DEEP", 1)

    AAA_CLIENT_AGENT: Optional[str] = os.getenv(
        "AAA_CLIENT_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",  # noqa: E501
    )
    AAA_TOPIC_EXTRACT_ENDPOINT: Optional[str] = os.getenv(
        "AAA_TOPIC_EXTRACT_ENDPOINT", "http://localhost:8001/api/v1/topic/"
    )

    VERSION: Optional[str] = (
        version + ".001"
    )  # Change this micro version in the development process

    # class Config:
    #     case_sensitive = True
    #     # env_file = ROOT / 'config' / 'enviroment_variable' / '.env'
    #     # env_file_encoding = 'utf-8'


SETTINGS = Settings()
