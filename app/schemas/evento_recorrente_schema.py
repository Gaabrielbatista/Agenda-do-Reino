from marshmallow import Schema, fields, validate, validates, ValidationError, EXCLUDE


def _parse_time(value):
    if value is None:
        return None
    try:
        parts = str(value).split(':')
        if len(parts) not in (2, 3):
            raise ValueError
        int(parts[0]), int(parts[1])  # valida que são inteiros
        return value
    except (ValueError, AttributeError):
        raise ValidationError("Formato de hora inválido. Use HH:MM ou HH:MM:SS")


class EventoRecorrenteCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    titulo = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    descricao = fields.Str(load_default=None, allow_none=True)
    dia_semana = fields.Int(required=True, strict=True, validate=validate.Range(min=0, max=6))
    hora_inicio = fields.Str(required=True)
    hora_fim = fields.Str(load_default=None, allow_none=True)
    criado_por = fields.Int(required=True, strict=True)

    @validates('hora_inicio')
    def validate_hora_inicio(self, value):
        _parse_time(value)

    @validates('hora_fim')
    def validate_hora_fim(self, value):
        if value is not None:
            _parse_time(value)


class EventoRecorrenteUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    titulo = fields.Str(validate=validate.Length(min=1, max=200))
    descricao = fields.Str(allow_none=True)
    dia_semana = fields.Int(strict=True, validate=validate.Range(min=0, max=6))
    hora_inicio = fields.Str()
    hora_fim = fields.Str(allow_none=True)
    ativo = fields.Bool()

    @validates('hora_inicio')
    def validate_hora_inicio(self, value):
        _parse_time(value)

    @validates('hora_fim')
    def validate_hora_fim(self, value):
        if value is not None:
            _parse_time(value)