from datetime import datetime, time

from app.models.evento_excecao import EventoExcecao, ExcecaoTipo
from app.db.database import db


def _parse_datetime(value):
    if value is None or isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError(f"Formato de data inválido: '{value}'. Use ISO 8601")


def _parse_time(value):
    if value is None or isinstance(value, time):
        return value
    try:
        parts = value.split(':')
        if len(parts) == 2:
            return time(int(parts[0]), int(parts[1]))
        if len(parts) == 3:
            return time(int(parts[0]), int(parts[1]), int(parts[2]))
        raise ValueError
    except (ValueError, AttributeError):
        raise ValueError(f"Formato de hora inválido: '{value}'. Use HH:MM ou HH:MM:SS")


def _validate_tipo(value: str) -> ExcecaoTipo:
    try:
        return ExcecaoTipo[value.upper()]
    except (KeyError, AttributeError):
        raise ValueError(f"tipo inválido: '{value}'. Use 'cancelamento' ou 'remarcacao'")


class EventoExcecaoRepository:
    def get_all(self):
        return EventoExcecao.query.all()

    def get_by_id(self, id):
        return EventoExcecao.query.filter_by(id=id).first()

    def get_by_recorrente(self, evento_recorrente_id: int):
        """Retorna todas as exceções de um evento recorrente específico."""
        return EventoExcecao.query.filter_by(
            evento_recorrente_id=evento_recorrente_id
        ).all()

    def get_by_recorrente_e_data(self, evento_recorrente_id: int, data_original: datetime):
        """Verifica se já existe exceção para essa ocorrência específica."""
        return EventoExcecao.query.filter_by(
            evento_recorrente_id=evento_recorrente_id,
            data_original=data_original,
        ).first()

    def create(self, dados: dict) -> EventoExcecao:
        tipo = _validate_tipo(dados['tipo'])
        data_original = _parse_datetime(dados['data_original'])

        excecao = EventoExcecao(
            evento_recorrente_id=dados['evento_recorrente_id'],
            data_original=data_original,
            tipo=tipo,
            data_nova=_parse_datetime(dados.get('data_nova')),
            hora_nova_inicio=_parse_time(dados.get('hora_nova_inicio')),
            hora_nova_fim=_parse_time(dados.get('hora_nova_fim')),
            motivo=dados.get('motivo'),
            criado_por=dados.get('criado_por'),
        )
        db.session.add(excecao)
        db.session.commit()
        return excecao

    def update(self, excecao: EventoExcecao, dados: dict) -> EventoExcecao:
        """Apenas campos opcionais são editáveis após criação."""
        if 'motivo' in dados:
            excecao.motivo = dados['motivo']
        if 'data_nova' in dados:
            excecao.data_nova = _parse_datetime(dados['data_nova'])
        if 'hora_nova_inicio' in dados:
            excecao.hora_nova_inicio = _parse_time(dados['hora_nova_inicio'])
        if 'hora_nova_fim' in dados:
            excecao.hora_nova_fim = _parse_time(dados['hora_nova_fim'])
        db.session.commit()
        return excecao

    def delete(self, excecao: EventoExcecao) -> None:
        db.session.delete(excecao)
        db.session.commit()