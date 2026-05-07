from flask import Flask
from app.db.database import init_db

def create_app():
    app = Flask(__name__)
    init_db(app)
    
    # Blueprints
    # from app.controllers.event_controller import event_bp
    # app.register_blueprint(event_bp)

    from app.models import usuario, evento_normal, evento_recorrente

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')