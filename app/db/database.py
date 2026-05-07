from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from app.config.settings import Config

db = SQLAlchemy()

def init_db(app):
    app.config.from_object(Config)
    db.init_app(app)
    
    print("Banco configurado com sucesso!")