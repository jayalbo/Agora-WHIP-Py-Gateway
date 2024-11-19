import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
CERTIFICATE = os.getenv("CERTIFICATE", None)
CUSTOMER_ID = os.getenv("CUSTOMER_ID")
CUSTOMER_SECRET = os.getenv("CUSTOMER_SECRET")
