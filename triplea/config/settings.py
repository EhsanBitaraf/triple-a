import os
import pathlib
from typing import List, Optional

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator, Field
from dotenv import load_dotenv

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent
DB_ROOT_PATH = ROOT.parent / "database"

load_dotenv(ROOT / "config" / "environment_variable" / ".env", override=True)

# # print all environment variable
# for name, value in os.environ.items():
#     print("{0}: {1}".format(name, value))


class Settings(BaseSettings):
    # KETTESTISNO: str = Field(description='fdfs', default="/api/v1", env='MY_API_KEY')
    # API_V1_STR: str = Field(description='fdfs', default="/api/v1", env='MY_API_KEY')
    JWT_SECRET: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
    ALGORITHM: str = "HS256"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///example.db"
    # FIRST_SUPERUSER: EmailStr = "admin@recipeapi.com"
    FIRST_SUPERUSER_PW: str = "CHANGEME"

    # ---------------My Envirement Varable-------------------------------
    AAA_DB_TYPE: Optional[str] = os.getenv("TRIPLEA_DB_TYPE", "TinyDB")
    AAA_TINYDB_FILENAME: Optional[str] = os.getenv(
        "AAA_TINYDB_FILENAME", "default-tiny-db.json"
    )
    AAA_MONGODB_CONNECTION_URL: Optional[str] = os.getenv("AAA_MONGODB_CONNECTION_URL")
    AAA_MONGODB_DB_NAME: Optional[str] = os.getenv("AAA_MONGODB_DB_NAME")
    AAA_TPS_LIMIT: Optional[int] = os.getenv("AAA_TPS_LIMIT", 1)
    AAA_PROXY_HTTP: Optional[str] = os.getenv("AAA_PROXY_HTTP", "")
    AAA_PROXY_HTTPS: Optional[str] = os.getenv("AAA_PROXY_HTTPS", "")
    AAA_REFF_CRAWLER_DEEP: Optional[int] = os.getenv("AAA_REFF_CRAWLER_DEEP", 1)
    AAA_CITED_CRAWLER_DEEP: Optional[int] = os.getenv("AAA_CITED_CRAWLER_DEEP", 1)

    # class Config:
    #     case_sensitive = True
    #     # env_file = ROOT / 'config' / 'enviroment_variable' / '.env'
    #     # env_file_encoding = 'utf-8'


SETTINGS = Settings()
