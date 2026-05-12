from flask import Blueprint, jsonify, request
from app.services.usuario_service import UsuarioService

usuario_bp = Blueprint('usuario', __name__)
service = UsuarioService()


def _serialize_usuario(usuario):
    return {
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'tipo': usuario.tipo.value,
    }


@usuario_bp.route('/usuarios', methods=['GET'])
def get_all():
    usuarios = service.get_all()
    return jsonify([_serialize_usuario(u) for u in usuarios])


@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
def get_by_id(id):
    usuario = service.get_by_id(id)
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    return jsonify(_serialize_usuario(usuario))


@usuario_bp.route('/usuarios', methods=['POST'])
def create():
    dados = request.get_json()
    if not dados.get('nome'):
        return jsonify({'error': 'nome é obrigatório'}), 400
    if not dados.get('email'):
        return jsonify({'error': 'email é obrigatório'}), 400
    if not dados.get('senha'):
        return jsonify({'error': 'senha é obrigatório'}), 400
    if not dados.get('tipo'):
        return jsonify({'error': 'tipo é obrigatório'}), 400
    try:
        usuario = service.create(dados)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(_serialize_usuario(usuario)), 201


@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def update(id):
    dados = request.get_json()
    if not dados:
        return jsonify({'error': 'Body JSON obrigatório'}), 400
    try:
        usuario = service.update(id, dados)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    return jsonify(_serialize_usuario(usuario))


@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def delete(id):
    deletado = service.delete(id)
    if not deletado:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    return '', 204