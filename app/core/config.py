import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    DB_NAME: str = ""
    COLLECTION_NAME: str = ""

settings = Settings()
