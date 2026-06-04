from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError, EXCLUDE
from datetime import datetime


def _parse_datetime(value):
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValidationError("Formato inválido. Use ISO 8601 (ex: 2026-05-10T10:00:00)")


def _parse_time(value):
    if value is None:
        return None
    try:
        parts = str(value).split(':')
        if len(parts) not in (2, 3):
            raise ValueError
        int(parts[0]), int(parts[1])
        return value
    except (ValueError, AttributeError):
        raise ValidationError("Formato de hora inválido. Use HH:MM ou HH:MM:SS")


class EventoExcecaoCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    evento_recorrente_id = fields.Int(required=True, strict=True)
    data_original = fields.Str(required=True)
    tipo = fields.Str(required=True)
    data_nova = fields.Str(load_default=None, allow_none=True)
    hora_nova_inicio = fields.Str(load_default=None, allow_none=True)
    hora_nova_fim = fields.Str(load_default=None, allow_none=True)
    motivo = fields.Str(load_default=None, allow_none=True)
    criado_por = fields.Int(load_default=None, allow_none=True, strict=True)

    @validates('data_original')
    def validate_data_original(self, value):
        _parse_datetime(value)

    @validates('data_nova')
    def validate_data_nova(self, value):
        if value is not None:
            _parse_datetime(value)

    @validates('hora_nova_inicio')
    def validate_hora_nova_inicio(self, value):
        if value is not None:
            _parse_time(value)

    @validates('hora_nova_fim')
    def validate_hora_nova_fim(self, value):
        if value is not None:
            _parse_time(value)

    @validates('tipo')
    def validate_tipo(self, value):
        if str(value).lower() not in ('cancelamento', 'remarcacao'):
            raise ValidationError("tipo inválido. Use 'cancelamento' ou 'remarcacao'.")

    @validates_schema
    def validate_remarcacao(self, data, **kwargs):
        """Remarcação exige ao menos data_nova ou hora_nova_inicio."""
        if str(data.get('tipo')).lower() == 'remarcacao':
            if not data.get('data_nova') and not data.get('hora_nova_inicio'):
                raise ValidationError(
                    "Para remarcação, informe ao menos 'data_nova' ou 'hora_nova_inicio'.",
                    field_name='tipo',
                )


class EventoExcecaoUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    motivo = fields.Str(allow_none=True)
    data_nova = fields.Str(allow_none=True)
    hora_nova_inicio = fields.Str(allow_none=True)
    hora_nova_fim = fields.Str(allow_none=True)

    @validates('data_nova')
    def validate_data_nova(self, value):
        if value is not None:
            _parse_datetime(value)

    @validates('hora_nova_inicio')
    def validate_hora_nova_inicio(self, value):
        if value is not None:
            _parse_time(value)

    @validates('hora_nova_fim')
    def validate_hora_nova_fim(self, value):
        if value is not None:
            _parse_time(value)