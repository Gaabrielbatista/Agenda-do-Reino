from flask import Blueprint, jsonify, request
from app.services.evento_normal_service import EventoNormalService

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
def get_all():
    eventos = service.get_all()
    return jsonify([_serialize_evento(e) for e in eventos])

@evento_normal_bp.route('/eventos/normais/<int:id>', methods=['GET'])
def get_by_id(id):
    evento = service.get_by_id(id)
    if not evento:
        return jsonify({'error': 'Evento não encontrado'}), 404
    return jsonify(_serialize_evento(evento))

@evento_normal_bp.route('/eventos/normais', methods=['POST'])
def create():
    dados = request.get_json()
    if not dados.get('titulo'):
        return jsonify({'error': 'titulo é obrigatório'}), 400
    if not dados.get('data_inicio'):
        return jsonify({'error': 'data_inicio é obrigatório'}), 400
    if not dados.get('criado_por'):
        return jsonify({'error': 'criado_por é obrigatório'}), 400
    try:
        evento = service.create(dados)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(_serialize_evento(evento)), 201

@evento_normal_bp.route('/eventos/normais/<int:id>', methods=['PUT'])
def update(id):
    dados = request.get_json()
    if not dados:
        return jsonify({'error': 'Body JSON obrigatório'}), 400
    try:
        evento = service.update(id, dados)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    if not evento:
        return jsonify({'error': 'Evento não encontrado'}), 404
    return jsonify(_serialize_evento(evento))

@evento_normal_bp.route('/eventos/normais/<int:id>', methods=['DELETE'])
def delete(id):
    deletado = service.delete(id)
    if not deletado:
        return jsonify({'error': 'Evento não encontrado'}), 404
    return '', 204