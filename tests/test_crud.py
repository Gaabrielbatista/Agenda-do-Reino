"""
Testes de CRUD direto nos models (sem HTTP), cobrindo:
- Usuario, EventoNormal, EventoRecorrente, EventoExcecao
- Constraints (NOT NULL, UNIQUE)
- Cascades de FK
"""

from datetime import datetime, time

import pytest
from sqlalchemy.exc import IntegrityError

from app.db.database import db as _db
from app.models.evento_excecao import EventoExcecao, ExcecaoTipo
from app.models.evento_normal import EventoNormal, EventoStatus
from app.models.evento_recorrente import EventoRecorrente
from app.models.usuario import Usuario, UserType


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def commit_and_refresh(obj):
    _db.session.add(obj)
    _db.session.commit()
    _db.session.refresh(obj)
    return obj


# ---------------------------------------------------------------------------
# Usuario
# ---------------------------------------------------------------------------

class TestCRUDUsuario:

    def test_criar_usuario_admin(self):
        u = commit_and_refresh(Usuario(
            nome="Ana Admin", email="ana@test.com",
            senha_hash="hash", tipo=UserType.ADMIN,
        ))
        recuperado = _db.session.get(Usuario, u.id)
        assert recuperado.nome == "Ana Admin"
        assert recuperado.tipo == UserType.ADMIN

    def test_criar_usuario_membro(self):
        u = commit_and_refresh(Usuario(
            nome="Bob Membro", email="bob@test.com",
            senha_hash="hash", tipo=UserType.MEMBRO,
        ))
        assert _db.session.get(Usuario, u.id).tipo == UserType.MEMBRO

    def test_atualizar_nome(self, admin):
        admin.nome = "Admin Atualizado"
        _db.session.commit()
        assert _db.session.get(Usuario, admin.id).nome == "Admin Atualizado"

    def test_atualizar_email(self, admin):
        admin.email = "novo@test.com"
        _db.session.commit()
        assert _db.session.get(Usuario, admin.id).email == "novo@test.com"

    def test_deletar_usuario(self, admin):
        uid = admin.id
        _db.session.delete(admin)
        _db.session.commit()
        assert _db.session.get(Usuario, uid) is None

    def test_email_unico_rejeita_duplicata(self, admin):
        dup = Usuario(
            nome="Outro", email=admin.email,   # mesmo email
            senha_hash="hash", tipo=UserType.MEMBRO,
        )
        _db.session.add(dup)
        with pytest.raises(IntegrityError):
            _db.session.commit()
        _db.session.rollback()

    def test_dois_usuarios_emails_diferentes(self, admin, membro):
        assert admin.id != membro.id
        assert admin.email != membro.email


# ---------------------------------------------------------------------------
# EventoNormal
# ---------------------------------------------------------------------------

class TestCRUDEventoNormal:

    def _make_evento(self, usuario_id, **kwargs):
        defaults = dict(
            titulo="Evento Teste",
            data_inicio=datetime(2025, 6, 1, 9, 0),
            status=EventoStatus.ATIVO,
            criado_por=usuario_id,
        )
        defaults.update(kwargs)
        return commit_and_refresh(EventoNormal(**defaults))

    def test_criar_evento_normal(self, admin):
        ev = self._make_evento(admin.id)
        assert _db.session.get(EventoNormal, ev.id).titulo == "Evento Teste"

    def test_criar_com_data_fim(self, admin):
        ev = self._make_evento(admin.id, data_fim=datetime(2025, 6, 1, 10, 0))
        assert _db.session.get(EventoNormal, ev.id).data_fim is not None

    def test_criar_sem_data_fim(self, admin):
        ev = self._make_evento(admin.id, data_fim=None)
        assert _db.session.get(EventoNormal, ev.id).data_fim is None

    def test_atualizar_titulo(self, admin):
        ev = self._make_evento(admin.id)
        ev.titulo = "Título Atualizado"
        _db.session.commit()
        assert _db.session.get(EventoNormal, ev.id).titulo == "Título Atualizado"

    def test_cancelar_evento(self, admin):
        ev = self._make_evento(admin.id)
        ev.status = EventoStatus.CANCELADO
        _db.session.commit()
        assert _db.session.get(EventoNormal, ev.id).status == EventoStatus.CANCELADO

    def test_deletar_evento_normal(self, admin):
        ev = self._make_evento(admin.id)
        eid = ev.id
        _db.session.delete(ev)
        _db.session.commit()
        assert _db.session.get(EventoNormal, eid) is None

    def test_cascade_deleta_eventos_ao_deletar_usuario(self, admin):
        ev = self._make_evento(admin.id)
        eid = ev.id
        _db.session.delete(admin)
        _db.session.commit()
        assert _db.session.get(EventoNormal, eid) is None


# ---------------------------------------------------------------------------
# EventoRecorrente
# ---------------------------------------------------------------------------

class TestCRUDEventoRecorrente:

    def _make_recorrente(self, usuario_id, **kwargs):
        defaults = dict(
            titulo="Reunião",
            dia_semana=0,
            hora_inicio=time(10, 0),
            ativo=True,
            criado_por=usuario_id,
        )
        defaults.update(kwargs)
        return commit_and_refresh(EventoRecorrente(**defaults))

    def test_criar_evento_recorrente(self, admin):
        ev = self._make_recorrente(admin.id)
        assert _db.session.get(EventoRecorrente, ev.id).dia_semana == 0

    def test_criar_com_hora_fim(self, admin):
        ev = self._make_recorrente(admin.id, hora_fim=time(11, 0))
        assert _db.session.get(EventoRecorrente, ev.id).hora_fim == time(11, 0)

    def test_desativar_evento(self, admin):
        ev = self._make_recorrente(admin.id)
        ev.ativo = False
        _db.session.commit()
        assert _db.session.get(EventoRecorrente, ev.id).ativo is False

    def test_atualizar_dia_semana(self, admin):
        ev = self._make_recorrente(admin.id)
        ev.dia_semana = 4  # sexta
        _db.session.commit()
        assert _db.session.get(EventoRecorrente, ev.id).dia_semana == 4

    def test_deletar_evento_recorrente(self, admin):
        ev = self._make_recorrente(admin.id)
        eid = ev.id
        _db.session.delete(ev)
        _db.session.commit()
        assert _db.session.get(EventoRecorrente, eid) is None

    def test_cascade_deleta_recorrentes_ao_deletar_usuario(self, admin):
        ev = self._make_recorrente(admin.id)
        eid = ev.id
        _db.session.delete(admin)
        _db.session.commit()
        assert _db.session.get(EventoRecorrente, eid) is None


# ---------------------------------------------------------------------------
# EventoExcecao
# ---------------------------------------------------------------------------

class TestCRUDEventoExcecao:

    def test_criar_excecao_cancelamento(self, evento_rec_segunda):
        exc = commit_and_refresh(EventoExcecao(
            evento_recorrente_id=evento_rec_segunda.id,
            data_original=datetime(2025, 1, 6, 10, 0),
            tipo=ExcecaoTipo.CANCELAMENTO,
        ))
        recuperado = _db.session.get(EventoExcecao, exc.id)
        assert recuperado.tipo == ExcecaoTipo.CANCELAMENTO
        assert recuperado.data_nova is None

    def test_criar_excecao_remarcacao(self, evento_rec_segunda):
        exc = commit_and_refresh(EventoExcecao(
            evento_recorrente_id=evento_rec_segunda.id,
            data_original=datetime(2025, 1, 6, 10, 0),
            tipo=ExcecaoTipo.REMARCACAO,
            data_nova=datetime(2025, 1, 8, 14, 0),
            hora_nova_inicio=time(14, 0),
            hora_nova_fim=time(15, 0),
            motivo="Feriado antecipado",
        ))
        recuperado = _db.session.get(EventoExcecao, exc.id)
        assert recuperado.tipo == ExcecaoTipo.REMARCACAO
        assert recuperado.hora_nova_inicio == time(14, 0)
        assert recuperado.motivo == "Feriado antecipado"

    def test_deletar_excecao(self, evento_rec_segunda):
        exc = commit_and_refresh(EventoExcecao(
            evento_recorrente_id=evento_rec_segunda.id,
            data_original=datetime(2025, 1, 6, 10, 0),
            tipo=ExcecaoTipo.CANCELAMENTO,
        ))
        eid = exc.id
        _db.session.delete(exc)
        _db.session.commit()
        assert _db.session.get(EventoExcecao, eid) is None

    def test_multiplas_excecoes_no_mesmo_evento(self, evento_rec_segunda):
        for dia in [6, 13, 20]:
            _db.session.add(EventoExcecao(
                evento_recorrente_id=evento_rec_segunda.id,
                data_original=datetime(2025, 1, dia, 10, 0),
                tipo=ExcecaoTipo.CANCELAMENTO,
            ))
        _db.session.commit()

        excecoes = EventoExcecao.query.filter_by(
            evento_recorrente_id=evento_rec_segunda.id
        ).all()
        assert len(excecoes) == 3

    def test_cascade_deleta_excecoes_ao_deletar_recorrente(self, evento_rec_segunda):
        exc = commit_and_refresh(EventoExcecao(
            evento_recorrente_id=evento_rec_segunda.id,
            data_original=datetime(2025, 1, 6, 10, 0),
            tipo=ExcecaoTipo.CANCELAMENTO,
        ))
        eid = exc.id

        _db.session.delete(evento_rec_segunda)
        _db.session.commit()
        assert _db.session.get(EventoExcecao, eid) is None