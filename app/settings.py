import os

from dotenv import load_dotenv


load_dotenv()


REQUEST_URL = "https://youtube.com"

REQUEST_LOGIN = os.getenv("REQUEST_LOGIN", None)

REQUEST_PASSWORD = os.getenv("REQUEST_PASSWORD", None)

DB_URL = os.getenv("DB_URL", "sqlite:///database.db")

MULTITHREADING = True

TIMEOUT = 10
