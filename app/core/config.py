import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Book Library Management API"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./library.db")
    JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_ME")
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

settings = Settings()
