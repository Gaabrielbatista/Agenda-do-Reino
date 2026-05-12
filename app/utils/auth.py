import jwt
import os
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import request, jsonify, g


SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-inseguro')
EXPIRACAO_HORAS = 24


def gerar_token(usuario_id: int, tipo: str) -> str:
    payload = {
        'sub': str(usuario_id),
        'tipo': tipo,
        'exp': datetime.now(timezone.utc) + timedelta(hours=EXPIRACAO_HORAS),
        'iat': datetime.now(timezone.utc),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def _extrair_payload():
    """Extrai e valida o token do header Authorization. Retorna payload ou None."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None, 'Token ausente ou formato inválido. Use: Bearer <token>'
    token = auth_header.split(' ', 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, 'Token expirado. Faça login novamente'
    except jwt.InvalidTokenError:
        return None, 'Token inválido'


def requer_auth(f):
    """Qualquer usuário autenticado (admin ou membro)."""
    @wraps(f)
    def decorated(*args, **kwargs):
        payload, erro = _extrair_payload()
        if erro:
            return jsonify({'error': erro}), 401
        # Disponibiliza o payload para a rota via flask.g
        g.usuario_id = int(payload['sub'])
        g.usuario_tipo = payload['tipo']
        return f(*args, **kwargs)
    return decorated


def requer_admin(f):
    """Apenas usuários com tipo ADMIN."""
    @wraps(f)
    def decorated(*args, **kwargs):
        payload, erro = _extrair_payload()
        if erro:
            return jsonify({'error': erro}), 401
        if payload['tipo'].upper() != 'ADMIN':
            return jsonify({'error': 'Acesso restrito a administradores'}), 403
        g.usuario_id = int(payload['sub'])
        g.usuario_tipo = payload['tipo']
        return f(*args, **kwargs)
    return decorated