import marshmallow as ma
import marshmallow.validate as va


class SearchSchema(ma.Schema):
    username = ma.fields.String(required=True, validate=va.Length(min=1, max=64))
    pattern = ma.fields.String(required=True, validate=va.Length(min=1))
