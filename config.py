import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "api/database", "quicksign.sqlite3")

# Criar diretório se não existir
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

class Config:
  SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"

  SQLALCHEMY_TRACK_MODIFICATIONS = False

  DEBUG = os.environ.get('FLASK_DEBUG', True) 

  
