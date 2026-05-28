from flask import Blueprint, jsonify, g
from app.services.evento_normal_service import EventoNormalService
from app.utils.auth import requer_auth, requer_admin
from app.utils.validation import validate_body
from app.schemas import EventoNormalCreateSchema, EventoNormalUpdateSchema

evento_normal_bp = Blueprint('evento_normal', __name__)
service = EventoNormalService()


def _serialize_evento(evento):
    return {
        'id': evento.id,
        'titulo': evento.titulo,
        'descricao': evento.descricao,
        'data_inicio': evento.data_inicio.isoformat() if evento.data_inicio else None,
        'data_fim': evento.data_fim.isoformat() if evento.data_fim else None,
        'status': evento.status.value,
        'criado_por': evento.criado_por,
    }


@evento_normal_bp.route('/eventos/normais', methods=['GET'])
@requer_auth
def get_all():
    eventos = service.get_all()
    return jsonify([_serialize_evento(e) for e in eventos])


@evento_normal_bp.route('/eventos/normais/<int:id>', methods=['GET'])
@requer_auth
def get_by_id(id):
    evento = service.get_by_id(id)
    if not evento:
        return jsonify({'error': 'Evento não encontrado'}), 404
    return jsonify(_serialize_evento(evento))


@evento_normal_bp.route('/eventos/normais', methods=['POST'])
@requer_admin
@validate_body(EventoNormalCreateSchema)
def create():
    try:
        evento = service.create(g.validated_data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(_serialize_evento(evento)), 201


@evento_normal_bp.route('/eventos/normais/<int:id>', methods=['PUT'])
@requer_admin
@validate_body(EventoNormalUpdateSchema)
def update(id):
    try:
        evento = service.update(id, g.validated_data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    if not evento:
        return jsonify({'error': 'Evento não encontrado'}), 404
    return jsonify(_serialize_evento(evento))


@evento_normal_bp.route('/eventos/normais/<int:id>', methods=['DELETE'])
@requer_admin
def delete(id):
    deletado = service.delete(id)
    if not deletado:
        return jsonify({'error': 'Evento não encontrado'}), 404
    return '', 204