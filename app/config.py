import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG ={
    'host' : os.environ.get('DB_HOST','localhost'),
    'port' : int(os.environ.get('DB_PORT',5432)),
    'database' : os.environ.get('DB_NAME','ssis_db'),
    'user' : os.environ.get('DB_USER','postgres'),
    'password' : os.environ.get('DB_PASS','')

}

SECRET_KEY = os.environ.get('SECRET_KEY', '')