import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("config")

load_dotenv()


class Config:
    # Postgres
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    DB_URL: str = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your_secret_key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_SECONDS: int = int(os.getenv("JWT_EXPIRATION_SECONDS", 3600))

    # Mail
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME") # type: ignore
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")# type: ignore
    MAIL_FROM: str = os.getenv("MAIL_FROM")# type: ignore
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")# type: ignore
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", 587))
    MAIL_FROM_NAME: str = "Rest API Service"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True


    # Cloudinary
    CLD_NAME: str = os.getenv("CLD_NAME", "mockcloud")
    CLD_API_KEY: str = os.getenv("CLD_API_KEY", "mockapikey")
    CLD_API_SECRET: str = os.getenv("CLD_API_SECRET", "mockapisecret")


config = Config()