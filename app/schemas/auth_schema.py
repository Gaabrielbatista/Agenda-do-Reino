from marshmallow import Schema, fields, EXCLUDE

class LoginSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    email = fields.Email(required=True)
    senha = fields.Str(required=True, load_only=True)