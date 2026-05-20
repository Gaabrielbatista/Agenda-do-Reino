import bcrypt

from flask import Blueprint, jsonify, g

from app.models.usuario import Usuario
from app.utils.auth import gerar_token
from app.utils.validation import validate_body
from app.schemas import LoginSchema


# Gera UM hash falso válido na inicialização do módulo (executa apenas uma vez)
DUMMY_HASH = bcrypt.hashpw(b'senha_falsa', bcrypt.gensalt()).decode('utf-8')

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/login', methods=['POST'])
@validate_body(LoginSchema)
def login():
    dados = g.validated_data

    usuario = Usuario.query.filter_by(email=dados['email'].lower().strip()).first()

    # Mesmo se o usuário não existir, compara o hash para evitar timing attack
    senha_bytes = dados['senha'].encode('utf-8')
    hash_verificar = usuario.senha_hash.encode('utf-8') if usuario else DUMMY_HASH.encode('utf-8')
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