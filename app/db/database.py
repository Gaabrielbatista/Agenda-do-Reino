import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from app.config.settings import Config

db = SQLAlchemy()

def init_db(app):
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        for tentativa in range(10):
            try:
                db.create_all()
                print("Banco conectado e tabelas")
                break
            except OperationalError:
                print(f"Banco indisponível, tentativa {tentativa + 1}/10...")
                time.sleep(2)
        else:
            print("Não foi possível conectar ao banco após 10 tentativas")