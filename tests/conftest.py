import pytest
from datetime import time

from app.app import create_app
from app.db.database import db as _db
from app.models.usuario import Usuario, UserType
from app.models.evento_recorrente import EventoRecorrente


# App / DB

@pytest.fixture(scope="session")
def app():
    """
    Cria a aplicação uma única vez por sessão de testes apontando para
    SQLite em memória. O app_context fica ativo durante toda a sessão.
    """
    
    flask_app = create_app(test_config={
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_ENGINE_OPTIONS": {
            "connect_args": {"check_same_thread": False},
        },
    })

    ctx = flask_app.app_context()
    ctx.push()
    _db.create_all()
    
    _db.session.expire_on_commit = False

    yield flask_app

    _db.drop_all()
    ctx.pop()


@pytest.fixture(autouse=True)
def clean_tables(app):  # noqa: ARG001
    """
    Apaga todas as linhas entre testes.
    Roda antes (setup vazio) e depois (teardown) de cada teste.
    """
    yield
    _db.session.rollback()
    for table in reversed(_db.metadata.sorted_tables):
        _db.session.execute(table.delete())
    _db.session.commit()
    # Limpa o cache de objetos da sessão
    _db.session.expunge_all()


@pytest.fixture
def client(app):
    return app.test_client()


# Objetos de domínio reutilizáveis

@pytest.fixture
def admin():
    """Usuário administrador persistido."""
    u = Usuario(
        nome="Admin Teste",
        email="admin@test.com",
        senha_hash="$2b$12$fakehashfakehashfake.",
        tipo=UserType.ADMIN,
    )
    _db.session.add(u)
    _db.session.commit()
    _db.session.refresh(u)
    return u


@pytest.fixture
def membro():
    """Usuário membro persistido."""
    u = Usuario(
        nome="Membro Teste",
        email="membro@test.com",
        senha_hash="$2b$12$fakehashfakehashfake.",
        tipo=UserType.MEMBRO,
    )
    _db.session.add(u)
    _db.session.commit()
    _db.session.refresh(u)
    return u


@pytest.fixture
def evento_rec_segunda(admin):
    """
    EventoRecorrente toda segunda-feira às 10h–11h.
    2025-01-06 (segunda) é o ponto de referência nos testes de recorrência.
    """
    ev = EventoRecorrente(
        titulo="Reunião Semanal",
        descricao="Toda segunda",
        dia_semana=0,          # 0 = segunda-feira
        hora_inicio=time(10, 0),
        hora_fim=time(11, 0),
        ativo=True,
        criado_por=admin.id,
    )
    _db.session.add(ev)
    _db.session.commit()
    _db.session.refresh(ev)
    return ev