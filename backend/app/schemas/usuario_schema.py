from marshmallow import Schema, fields, validate, validates, ValidationError, EXCLUDE


class UsuarioCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    nome = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    email = fields.Email(required=True)
    senha = fields.Str(required=True, validate=validate.Length(min=6), load_only=True)
    tipo = fields.Str(required=True, validate=validate.OneOf(['admin', 'membro']))

    @validates('nome')
    def validate_nome(self, value):
        if not value.strip():
            raise ValidationError('nome não pode ser vazio ou apenas espaços.')
        return value.strip()


class UsuarioUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    nome = fields.Str(validate=validate.Length(min=2, max=120))
    email = fields.Email()
    senha = fields.Str(validate=validate.Length(min=6), load_only=True)
    tipo = fields.Str(validate=validate.OneOf(['admin', 'membro']))


class UsuarioResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str()
    email = fields.Email()
    tipo = fields.Str()