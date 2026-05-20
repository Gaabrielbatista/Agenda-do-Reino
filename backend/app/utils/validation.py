from functools import wraps
from flask import request, jsonify, g
from marshmallow import ValidationError


def validate_body(schema_class):
    """
    Decorator que valida o JSON do request contra um Schema Marshmallow.
    Em caso de erro, retorna 400 com os detalhes.
    Em caso de sucesso, injeta os dados validados em g.validated_data.

    Uso:
        @validate_body(UsuarioCreateSchema)
        def create():
            dados = g.validated_data
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            body = request.get_json(silent=True)
            if body is None:
                return jsonify({'error': 'Body JSON obrigatório'}), 400
            schema = schema_class()
            try:
                g.validated_data = schema.load(body)
            except ValidationError as err:
                return jsonify({'error': 'Dados inválidos', 'detalhes': err.messages}), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator