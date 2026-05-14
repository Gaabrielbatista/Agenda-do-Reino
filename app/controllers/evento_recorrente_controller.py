from flask import Blueprint, jsonify, g
from app.services.evento_recorrente_service import EventoRecorrenteService
from app.utils.auth import requer_auth, requer_admin
from app.utils.validation import validate_body
from app.schemas import EventoRecorrenteCreateSchema, EventoRecorrenteUpdateSchema

evento_recorrente_bp = Blueprint('evento_recorrente', __name__)
service = EventoRecorrenteService()

DIAS_SEMANA = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo']


def _serialize_evento(evento):
    return {
        'id': evento.id,
        'titulo': evento.titulo,
        'descricao': evento.descricao,
        'dia_semana': evento.dia_semana,
        'dia_semana_nome': DIAS_SEMANA[evento.dia_semana],
        'hora_inicio': evento.hora_inicio.strftime('%H:%M') if evento.hora_inicio else None,
        'hora_fim': evento.hora_fim.strftime('%H:%M') if evento.hora_fim else None,
        'ativo': evento.ativo,
        'criado_por': evento.criado_por,
    }


@evento_recorrente_bp.route('/eventos/recorrentes', methods=['GET'])
@requer_auth
def get_all():
    eventos = service.get_all()
    return jsonify([_serialize_evento(e) for e in eventos])


@evento_recorrente_bp.route('/eventos/recorrentes/<int:id>', methods=['GET'])
@requer_auth
def get_by_id(id):
    evento = service.get_by_id(id)
    if not evento:
        return jsonify({'error': 'Evento não encontrado'}), 404
    return jsonify(_serialize_evento(evento))


@evento_recorrente_bp.route('/eventos/recorrentes', methods=['POST'])
@requer_admin
@validate_body(EventoRecorrenteCreateSchema)
def create():
    try:
        evento = service.create(g.validated_data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(_serialize_evento(evento)), 201


@evento_recorrente_bp.route('/eventos/recorrentes/<int:id>', methods=['PUT'])
@requer_admin
@validate_body(EventoRecorrenteUpdateSchema)
def update(id):
    try:
        evento = service.update(id, g.validated_data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    if not evento:
        return jsonify({'error': 'Evento não encontrado'}), 404
    return jsonify(_serialize_evento(evento))


@evento_recorrente_bp.route('/eventos/recorrentes/<int:id>', methods=['DELETE'])
@requer_admin
def delete(id):
    deletado = service.delete(id)
    if not deletado:
        return jsonify({'error': 'Evento não encontrado'}), 404
    return '', 204