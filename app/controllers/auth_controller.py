import bcrypt

from flask import Blueprint, jsonify, request

from app.models.usuario import Usuario
from app.utils.auth import gerar_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    dados = request.get_json()
    if not dados.get('email'):
        return jsonify({'error': 'email é obrigatório'}), 400
    if not dados.get('senha'):
        return jsonify({'error': 'senha é obrigatório'}), 400

    usuario = Usuario.query.filter_by(email=dados['email'].lower().strip()).first()

    # Mesmo se o usuário não existir, compara o hash para evitar timing attack
    senha_bytes = dados['senha'].encode('utf-8')
    hash_verificar = usuario.senha_hash.encode('utf-8') if usuario else b'$2b$12$invalido.hash.para.timing'

    senha_valida = bcrypt.checkpw(senha_bytes, hash_verificar)

    if not usuario or not senha_valida:
        return jsonify({'error': 'Email ou senha inválidos'}), 401

    token = gerar_token(usuario.id, usuario.tipo.value)

    return jsonify({
        'token': token,
        'usuario': {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'tipo': usuario.tipo.value,
        }
    })