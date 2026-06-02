from flask import Blueprint, jsonify, g
from app.services.evento_excecao_service import EventoExcecaoService
from app.utils.auth import requer_auth, requer_admin
from app.utils.validation import validate_body
from app.schemas.evento_excecao_schema import EventoExcecaoCreateSchema, EventoExcecaoUpdateSchema

evento_excecao_bp = Blueprint('evento_excecao', __name__)
service = EventoExcecaoService()


def _serialize(excecao):
    return {
        'id': excecao.id,
        'evento_recorrente_id': excecao.evento_recorrente_id,
        'data_original': excecao.data_original.isoformat() if excecao.data_original else None,
        'tipo': excecao.tipo.name,
        'data_nova': excecao.data_nova.isoformat() if excecao.data_nova else None,
        'hora_nova_inicio': excecao.hora_nova_inicio.strftime('%H:%M') if excecao.hora_nova_inicio else None,
        'hora_nova_fim': excecao.hora_nova_fim.strftime('%H:%M') if excecao.hora_nova_fim else None,
        'motivo': excecao.motivo,
        'criado_por': excecao.criado_por,
    }


@evento_excecao_bp.route('/eventos/excecoes', methods=['GET'])
@requer_auth
def get_all():
    excecoes = service.get_all()
    return jsonify([_serialize(e) for e in excecoes])


@evento_excecao_bp.route('/eventos/excecoes/<int:id>', methods=['GET'])
@requer_auth
def get_by_id(id):
    excecao = service.get_by_id(id)
    if not excecao:
        return jsonify({'error': 'Exceção não encontrada'}), 404
    return jsonify(_serialize(excecao))


@evento_excecao_bp.route('/eventos/recorrentes/<int:recorrente_id>/excecoes', methods=['GET'])
@requer_auth
def get_by_recorrente(recorrente_id):
    """Lista todas as exceções de um evento recorrente específico."""
    excecoes = service.get_by_recorrente(recorrente_id)
    return jsonify([_serialize(e) for e in excecoes])


@evento_excecao_bp.route('/eventos/excecoes', methods=['POST'])
@requer_admin
@validate_body(EventoExcecaoCreateSchema)
def create():
    try:
        excecao = service.create(g.validated_data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(_serialize(excecao)), 201


@evento_excecao_bp.route('/eventos/excecoes/<int:id>', methods=['PUT'])
@requer_admin
@validate_body(EventoExcecaoUpdateSchema)
def update(id):
    try:
        excecao = service.update(id, g.validated_data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    if not excecao:
        return jsonify({'error': 'Exceção não encontrada'}), 404
    return jsonify(_serialize(excecao))


@evento_excecao_bp.route('/eventos/excecoes/<int:id>', methods=['DELETE'])
@requer_admin
def delete(id):
    deletado = service.delete(id)
    if not deletado:
        return jsonify({'error': 'Exceção não encontrada'}), 404
    return '', 204