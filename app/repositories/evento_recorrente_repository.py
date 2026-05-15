from datetime import time

from app.models.evento_recorrente import EventoRecorrente
from app.db.database import db


def _parse_time(value):
    """Aceita time ou string HH:MM ou HH:MM:SS; retorna time ou None."""
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


def _validate_dia_semana(value):
    """0 = segunda ... 6 = domingo."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValueError("dia_semana deve ser um inteiro")
    if value < 0 or value > 6:
        raise ValueError(f"dia_semana inválido: '{value}'. Use 0 (segunda) a 6 (domingo)")
    return value


class EventoRecorrenteRepository:
    def get_all(self):
        return EventoRecorrente.query.all()

    def get_by_id(self, id):
        return EventoRecorrente.query.filter_by(id=id).first()

    def create(self, dados):
        evento = EventoRecorrente(
            titulo=dados['titulo'],
            descricao=dados.get('descricao'),
            dia_semana=_validate_dia_semana(dados['dia_semana']),
            hora_inicio=_parse_time(dados['hora_inicio']),
            hora_fim=_parse_time(dados.get('hora_fim')),
            criado_por=dados['criado_por']
            # ativo default=True definido no model
        )
        db.session.add(evento)
        db.session.commit()
        return evento

    def update(self, evento: EventoRecorrente, dados: dict) -> EventoRecorrente:
        """Recebe o objeto já carregado — sem query extra."""
        if 'titulo' in dados:
            evento.titulo = dados['titulo']
        if 'descricao' in dados:
            evento.descricao = dados['descricao']  # None limpa o campo, intencional
        if 'dia_semana' in dados:
            evento.dia_semana = _validate_dia_semana(dados['dia_semana'])
        if 'hora_inicio' in dados:
            evento.hora_inicio = _parse_time(dados['hora_inicio'])
        if 'hora_fim' in dados:
            evento.hora_fim = _parse_time(dados['hora_fim'])
        if 'ativo' in dados:
            if not isinstance(dados['ativo'], bool):
                raise ValueError("ativo deve ser true ou false")
            evento.ativo = dados['ativo']
        # criado_por é imutável — ignorado mesmo que venha no payload
        db.session.commit()
        return evento

    def delete(self, evento: EventoRecorrente) -> None:
        """Recebe o objeto já carregado — sem query extra."""
        db.session.delete(evento)
        db.session.commit()