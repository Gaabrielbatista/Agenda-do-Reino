from datetime import datetime

from app.models.evento_normal import EventoNormal, EventoStatus
from app.db.database import db


def _parse_datetime(value):
    """Aceita datetime ou string ISO 8601; retorna datetime ou None."""
    if value is None or isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError(f"Formato de data inválido: '{value}'. Use ISO 8601 (ex: 2026-05-10T10:00:00)")


class EventoNormalRepository:
    def get_all(self):
        return EventoNormal.query.all()

    def get_by_id(self, id):
        return EventoNormal.query.filter_by(id=id).first()

    def create(self, dados):
        evento = EventoNormal(
            titulo=dados['titulo'],
            descricao=dados.get('descricao'),
            data_inicio=_parse_datetime(dados['data_inicio']),
            data_fim=_parse_datetime(dados.get('data_fim')),
            criado_por=dados['criado_por']
        )
        db.session.add(evento)
        db.session.commit()
        return evento

    def update(self, evento: EventoNormal, dados: dict) -> EventoNormal:
        """Recebe o objeto já carregado — sem query extra."""
        if 'titulo' in dados:
            evento.titulo = dados['titulo']
        if 'descricao' in dados:
            evento.descricao = dados['descricao']  # None limpa o campo, intencional
        if 'data_inicio' in dados:
            evento.data_inicio = _parse_datetime(dados['data_inicio'])
        if 'data_fim' in dados:
            evento.data_fim = _parse_datetime(dados['data_fim'])
        if 'status' in dados:
            status_raw = dados['status']
            if isinstance(status_raw, str):
                try:
                    evento.status = EventoStatus[status_raw.upper()]
                except KeyError:
                    valores = [e.name for e in EventoStatus]
                    raise ValueError(f"status inválido: '{status_raw}'. Valores aceitos: {valores}")
            else:
                evento.status = status_raw
        # criado_por é imutável — ignorado mesmo que venha no payload
        db.session.commit()
        return evento

    def delete(self, evento: EventoNormal) -> None:
        """Recebe o objeto já carregado — sem query extra."""
        db.session.delete(evento)
        db.session.commit()