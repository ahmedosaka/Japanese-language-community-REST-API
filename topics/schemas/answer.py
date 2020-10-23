from marshmallow import Schema, fields, post_dump
from auth.schemas.user import UserSchema


class AnswerSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    contents = fields.String(required=True)
    published_date = fields.DateTime(dump_only=True)
    author = fields.Nested(UserSchema, attribute="m_user", dump_only=True, only=['id', 'username'])

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'answers': data}
        return data
