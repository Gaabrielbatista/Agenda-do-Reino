from flask import Flask
from app.db.database import init_db

def create_app(test_config=None):
    app = Flask(__name__)
    init_db(app, test_config)
    
    # Blueprints
    from app.controllers.evento_normal_controller import evento_normal_bp
    from app.controllers.evento_recorrente_controller import evento_recorrente_bp
    from app.controllers.evento_excecao_controller import evento_excecao_bp
    from app.controllers.usuario_controller import usuario_bp
    from app.controllers.agenda_controller import agenda_bp
    from app.controllers.auth_controller import auth_bp

    app.register_blueprint(evento_normal_bp)
    app.register_blueprint(evento_recorrente_bp)
    app.register_blueprint(evento_excecao_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(agenda_bp)
    app.register_blueprint(auth_bp)

    app.json.sort_keys = False

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')