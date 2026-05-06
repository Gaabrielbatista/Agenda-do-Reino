from flask import Flask
from app.db.database import init_db

def create_app():
    app = Flask(__name__)
    
    # Inicializa o banco
    init_db(app)
    
    # Registra blueprints (rotas) aqui futuramente
    # from app.controllers.event_controller import event_bp
    # app.register_blueprint(event_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')