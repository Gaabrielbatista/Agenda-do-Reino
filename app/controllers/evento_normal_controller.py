from flask import Blueprint, jsonify
from app.services.evento_normal_service import EventoNormalService

evento_normal_bp = Blueprint('evento_normal', __name__)
service = EventoNormalService()

@evento_normal_bp.route('/eventos/normais', methods=['GET'])
def get_all():
    eventos = service.listar_todos()

    return jsonify([{
        'id': e.id,
        'titulo': e.titulo,
        'descricao': e.descricao,
        'data_inicio': e.data_inicio.isoformat() if e.data_inicio else None,
        'data_fim': e.data_fim.isoformat() if e.data_fim else None,
        'status': e.status.value,
    } for e in eventos])