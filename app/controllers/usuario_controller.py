from flask import Blueprint, jsonify, g
from app.services.usuario_service import UsuarioService
from app.utils.auth import requer_auth, requer_admin
from app.utils.validation import validate_body
from app.schemas import UsuarioCreateSchema, UsuarioUpdateSchema

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
@requer_auth
def get_all():
    usuarios = service.get_all()
    return jsonify([_serialize_usuario(u) for u in usuarios])


@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
@requer_auth
def get_by_id(id):
    usuario = service.get_by_id(id)
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    return jsonify(_serialize_usuario(usuario))


@usuario_bp.route('/usuarios', methods=['POST'])
@requer_admin
@validate_body(UsuarioCreateSchema)
def create():
    try:
        usuario = service.create(g.validated_data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(_serialize_usuario(usuario)), 201


@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
@requer_admin
@validate_body(UsuarioUpdateSchema)
def update(id):
    try:
        usuario = service.update(id, g.validated_data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    return jsonify(_serialize_usuario(usuario))


@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
@requer_admin
def delete(id):
    deletado = service.delete(id)
    if not deletado:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    return '', 204