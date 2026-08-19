import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'campuspulse_secret_key_2026_host_portal')
    
    # MySQL Database Config
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'campuspulse_db')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))

    # SQLite Dev Fallback
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLITE_DB_PATH = os.path.join(BASE_DIR, 'campuspulse.db')
    
    # Uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
