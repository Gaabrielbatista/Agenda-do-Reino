import os

from app.app import create_app
from app.repositories.usuario_repository import UsuarioRepository

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

FLASK_ENV = os.getenv("FLASK_ENV", "development")


if not all([ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD]):
    if FLASK_ENV == 'production':
        raise RuntimeError("Dados de ADMIN não definidos no ambiente de produção. Defina ADMIN_USERNAME, ADMIN_EMAIL e ADMIN_PASSWORD.")
    else:
        print("WARNING: Dados de ADMIN não definidos. Usando credenciais padrão de desenvolvimento.")
        ADMIN_USERNAME = "Administrador"
        ADMIN_EMAIL = "admin@example.com"
        ADMIN_PASSWORD = "password123"

app = create_app()
with app.app_context():
    repo = UsuarioRepository()

    usuario_existente = repo.get_by_email(ADMIN_EMAIL)

    if usuario_existente:
        print(f"Admin já existe com o e-mail {ADMIN_EMAIL}. Pulando criação.")
    else:
        repo.create({
            "nome": ADMIN_USERNAME,
            "email": ADMIN_EMAIL,
            "senha": ADMIN_PASSWORD,
            "tipo": "admin"
        })
        print(f"Admin criado com sucesso: {ADMIN_EMAIL}")