"""
Testes do motor de recorrência: utils/recurrence.py → gerar_ocorrencias()

Datas de referência:
  - 2025-01-05 = domingo  (weekday 6)
  - 2025-01-06 = segunda  (weekday 0)  ← dia do evento_rec_segunda
  - 2025-01-07 = terça    (weekday 1)
  - 2025-01-08 = quarta   (weekday 2)
"""

from datetime import date, datetime, time, timedelta

import pytest

from app.db.database import db as _db
from app.models.evento_excecao import EventoExcecao, ExcecaoTipo
from app.models.evento_recorrente import EventoRecorrente
from app.utils.recurrence import gerar_ocorrencias

DOMINGO = date(2025, 1, 5)
SEGUNDA = date(2025, 1, 6)
TERCA   = date(2025, 1, 7)
QUARTA  = date(2025, 1, 8)


# Helpers

def add_excecao(**kwargs):
    exc = EventoExcecao(**kwargs)
    _db.session.add(exc)
    _db.session.commit()
    _db.session.refresh(exc)
    return exc


def ocorrencias(evento, inicio, semanas=0, fim=None):
    if fim is None:
        fim = inicio + timedelta(weeks=semanas)
    return gerar_ocorrencias(evento, inicio, fim)


# Geração básica

class TestGeracaoBasica:

    def test_evento_inativo_retorna_lista_vazia(self, evento_rec_segunda):
        evento_rec_segunda.ativo = False
        _db.session.commit()

        assert ocorrencias(evento_rec_segunda, SEGUNDA, semanas=3) == []

    def test_quatro_semanas_geram_quatro_ocorrencias(self, evento_rec_segunda):
        # 06, 13, 20, 27/jan
        resultado = ocorrencias(evento_rec_segunda, SEGUNDA, semanas=3)
        assert len(resultado) == 4

    def test_source_type_e_id_corretos(self, evento_rec_segunda):
        oc = ocorrencias(evento_rec_segunda, SEGUNDA, semanas=0)[0]
        assert oc["source_type"] == "recorrente"
        assert oc["source_id"] == evento_rec_segunda.id

    def test_data_inicio_e_fim_corretos(self, evento_rec_segunda):
        oc = ocorrencias(evento_rec_segunda, SEGUNDA, semanas=0)[0]
        assert oc["data_inicio"] == datetime(2025, 1, 6, 10, 0).isoformat()
        assert oc["data_fim"]    == datetime(2025, 1, 6, 11, 0).isoformat()

    def test_sem_hora_fim_retorna_none(self, admin):
        ev = EventoRecorrente(
            titulo="Evento sem fim",
            dia_semana=0,
            hora_inicio=time(9, 0),
            hora_fim=None,
            ativo=True,
            criado_por=admin.id,
        )
        _db.session.add(ev)
        _db.session.commit()

        oc = ocorrencias(ev, SEGUNDA, semanas=0)[0]
        assert oc["data_fim"] is None

    def test_titulo_e_descricao_propagados(self, evento_rec_segunda):
        oc = ocorrencias(evento_rec_segunda, SEGUNDA, semanas=0)[0]
        assert oc["titulo"] == "Reunião Semanal"
        assert oc["descricao"] == "Toda segunda"

    def test_excecao_id_none_para_ocorrencias_normais(self, evento_rec_segunda):
        oc = ocorrencias(evento_rec_segunda, SEGUNDA, semanas=0)[0]
        assert oc["excecao_id"] is None


# Cálculo do primeiro dia

class TestPrimeiroDia:

    def test_inicio_no_mesmo_dia_do_evento(self, evento_rec_segunda):
        # início = segunda → inclui a própria segunda
        resultado = ocorrencias(evento_rec_segunda, SEGUNDA, semanas=0)
        assert len(resultado) == 1
        assert "2025-01-06" in resultado[0]["data_inicio"]

    def test_inicio_antes_do_dia_semana(self, evento_rec_segunda):
        # início = domingo (5) → próxima segunda é dia 6
        resultado = ocorrencias(evento_rec_segunda, DOMINGO, fim=SEGUNDA)
        assert len(resultado) == 1
        assert "2025-01-06" in resultado[0]["data_inicio"]

    def test_inicio_apos_dia_semana_pula_para_proxima_semana(self, evento_rec_segunda):
        # início = terça (7) → próxima segunda é dia 13
        resultado = ocorrencias(evento_rec_segunda, TERCA, fim=TERCA + timedelta(days=6))
        assert len(resultado) == 1
        assert "2025-01-13" in resultado[0]["data_inicio"]

    def test_intervalo_sem_nenhuma_segunda(self, evento_rec_segunda):
        # Terça a sábado: nenhuma segunda
        resultado = ocorrencias(evento_rec_segunda, TERCA, fim=TERCA + timedelta(days=4))
        assert len(resultado) == 0

    def test_fim_exclusivo_nao_inclui_data_exata_no_dia_seguinte(self, evento_rec_segunda):
        # fim = domingo dia 12 → não deve incluir segunda dia 13
        resultado = ocorrencias(evento_rec_segunda, SEGUNDA, fim=SEGUNDA + timedelta(days=6))
        assert len(resultado) == 1


# Exceções: CANCELAMENTO

class TestCancelamento:

    def test_cancelamento_remove_ocorrencia(self, evento_rec_segunda):
        add_excecao(
            evento_recorrente_id=evento_rec_segunda.id,
            data_original=datetime(2025, 1, 6, 10, 0),
            tipo=ExcecaoTipo.CANCELAMENTO,
        )

        resultado = ocorrencias(evento_rec_segunda, SEGUNDA, semanas=1)
        # Semanas: 6 (cancelado) e 13 (normal)
        assert len(resultado) == 1
        assert "2025-01-13" in resultado[0]["data_inicio"]

    def test_cancelamento_nao_afeta_outras_semanas(self, evento_rec_segunda):
        add_excecao(
            evento_recorrente_id=evento_rec_segunda.id,
            data_original=datetime(2025, 1, 6, 10, 0),
            tipo=ExcecaoTipo.CANCELAMENTO,
        )

        resultado = ocorrencias(evento_rec_segunda, SEGUNDA, semanas=3)
        # 4 semanas - 1 cancelada = 3
        assert len(resultado) == 3

    def test_cancelamento_de_semana_fora_do_intervalo_nao_interfere(self, evento_rec_segunda):
        # Cancela dia 13, mas o intervalo só cobre dia 6
        add_excecao(
            evento_recorrente_id=evento_rec_segunda.id,
            data_original=datetime(2025, 1, 13, 10, 0),
            tipo=ExcecaoTipo.CANCELAMENTO,
        )

        resultado = ocorrencias(evento_rec_segunda, SEGUNDA, semanas=0)
        assert len(resultado) == 1


# Exceções: REMARCAÇÃO

class TestRemarcacao:

    def test_remarcacao_com_data_nova(self, evento_rec_segunda):
        exc = add_excecao(
            evento_recorrente_id=evento_rec_segunda.id,
            data_original=datetime(2025, 1, 6, 10, 0),
            tipo=ExcecaoTipo.REMARCACAO,
            data_nova=datetime(2025, 1, 8, 14, 0),   # quarta às 14h
            hora_nova_inicio=time(14, 0),
            hora_nova_fim=time(15, 0),
        )

        resultado = ocorrencias(evento_rec_segunda, SEGUNDA, semanas=0)
        assert len(resultado) == 1
        oc = resultado[0]
        assert oc["remarcado"] is True
        assert oc["excecao_id"] == exc.id
        assert "2025-01-08" in oc["data_inicio"]
        assert "14:00" in oc["data_inicio"]
        assert "15:00" in oc["data_fim"]

    def test_remarcacao_sem_data_nova_mantém_data_original(self, evento_rec_segunda):
        add_excecao(
            evento_recorrente_id=evento_rec_segunda.id,
            data_original=datetime(2025, 1, 6, 10, 0),
            tipo=ExcecaoTipo.REMARCACAO,
            data_nova=None,
            hora_nova_inicio=time(15, 0),   # só muda hora
            hora_nova_fim=time(16, 0),
        )

        oc = ocorrencias(evento_rec_segunda, SEGUNDA, semanas=0)[0]
        assert "2025-01-06" in oc["data_inicio"]   # data mantida
        assert "15:00"       in oc["data_inicio"]   # hora atualizada

    def test_remarcacao_sem_hora_nova_usa_hora_original(self, evento_rec_segunda):
        add_excecao(
            evento_recorrente_id=evento_rec_segunda.id,
            data_original=datetime(2025, 1, 6, 10, 0),
            tipo=ExcecaoTipo.REMARCACAO,
            data_nova=datetime(2025, 1, 8, 0, 0),   # outra data, mas sem hora_nova
            hora_nova_inicio=None,
            hora_nova_fim=None,
        )

        oc = ocorrencias(evento_rec_segunda, SEGUNDA, semanas=0)[0]
        assert "2025-01-08" in oc["data_inicio"]
        assert "10:00" in oc["data_inicio"]   # hora do evento original

    def test_remarcacao_marcada_como_remarcado(self, evento_rec_segunda):
        add_excecao(
            evento_recorrente_id=evento_rec_segunda.id,
            data_original=datetime(2025, 1, 6, 10, 0),
            tipo=ExcecaoTipo.REMARCACAO,
            hora_nova_inicio=time(9, 0),
        )

        oc = ocorrencias(evento_rec_segunda, SEGUNDA, semanas=0)[0]
        assert oc.get("remarcado") is True


# Cenários combinados

class TestCenariosCombinados:

    def test_cancelamento_e_remarcacao_na_mesma_janela(self, evento_rec_segunda):
        # Semana 1 (6/jan):  cancelado
        # Semana 2 (13/jan): remarcado para quarta
        # Semana 3 (20/jan): normal
        _db.session.add(EventoExcecao(
            evento_recorrente_id=evento_rec_segunda.id,
            data_original=datetime(2025, 1, 6, 10, 0),
            tipo=ExcecaoTipo.CANCELAMENTO,
        ))
        _db.session.add(EventoExcecao(
            evento_recorrente_id=evento_rec_segunda.id,
            data_original=datetime(2025, 1, 13, 10, 0),
            tipo=ExcecaoTipo.REMARCACAO,
            data_nova=datetime(2025, 1, 15, 9, 0),
            hora_nova_inicio=time(9, 0),
        ))
        _db.session.commit()

        resultado = ocorrencias(evento_rec_segunda, SEGUNDA, semanas=2)
        assert len(resultado) == 2    # semana 1 cancelada; 2 e 3 presentes

        remarcada = next(oc for oc in resultado if oc.get("remarcado"))
        normal    = next(oc for oc in resultado if not oc.get("remarcado"))

        assert "2025-01-15" in remarcada["data_inicio"]
        assert "09:00"      in remarcada["data_inicio"]
        assert "2025-01-20" in normal["data_inicio"]

    def test_excecoes_de_outro_evento_nao_interferem(self, admin, evento_rec_segunda):
        # Cria outro evento e cancela a mesma data → não deve afetar evento_rec_segunda
        outro = EventoRecorrente(
            titulo="Outro evento",
            dia_semana=0,
            hora_inicio=time(10, 0),
            ativo=True,
            criado_por=admin.id,
        )
        _db.session.add(outro)
        _db.session.commit()
        _db.session.refresh(outro)

        add_excecao(
            evento_recorrente_id=outro.id,
            data_original=datetime(2025, 1, 6, 10, 0),
            tipo=ExcecaoTipo.CANCELAMENTO,
        )

        resultado = ocorrencias(evento_rec_segunda, SEGUNDA, semanas=0)
        assert len(resultado) == 1