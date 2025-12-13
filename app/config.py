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

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

SECRET_KEY = os.environ.get('SECRET_KEY', '')

# Max file upload size: 5MB
MAX_CONTENT_LENGTH = 5 * 1024 * 1024