from config import Settings
from wallet_repository import AsyncTransactionRepository

settings = Settings()
db_config = {
    "user": settings.db_user,
    "password": settings.db_password,
    "host": settings.db_host,
    "port": settings.db_port,
    "database": settings.db_name
}

repository = AsyncTransactionRepository(db_config)

