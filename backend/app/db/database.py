from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from app.config.settings import Config

db = SQLAlchemy()

def init_db(app, test_config=None):
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    print("Banco configurado!")