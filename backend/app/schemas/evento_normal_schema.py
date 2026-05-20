from marshmallow import Schema, fields, validate, validates, ValidationError, EXCLUDE
from datetime import datetime


def _parse_datetime(value):
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValidationError("Formato inválido. Use ISO 8601 (ex: 2026-05-10T10:00:00)")


class EventoNormalCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    titulo = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    descricao = fields.Str(load_default=None, allow_none=True)
    data_inicio = fields.Str(required=True)   # validado em @validates
    data_fim = fields.Str(load_default=None, allow_none=True)
    criado_por = fields.Int(required=True, strict=True)

    @validates('data_inicio')
    def validate_data_inicio(self, value):
        _parse_datetime(value)  # lança ValidationError se inválido

    @validates('data_fim')
    def validate_data_fim(self, value):
        if value is not None:
            _parse_datetime(value)


class EventoNormalUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    titulo = fields.Str(validate=validate.Length(min=1, max=200))
    descricao = fields.Str(allow_none=True)
    data_inicio = fields.Str()
    data_fim = fields.Str(allow_none=True)
    status = fields.Str(validate=validate.OneOf(['ativo', 'cancelado']))

    @validates('data_inicio')
    def validate_data_inicio(self, value):
        _parse_datetime(value)

    @validates('data_fim')
    def validate_data_fim(self, value):
        if value is not None:
            _parse_datetime(value)