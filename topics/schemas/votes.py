from marshmallow import Schema, fields, post_dump
from auth.schemas.user import UserSchema
from topics.schemas.topics import TopicSchema
from topics.schemas.answer import AnswerSchema


class VotesSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    author = fields.Nested(UserSchema, attribute="m_user", dump_only=True, only=['id', 'username'])
    topic = fields.Nested(TopicSchema, attribute="t_topics", dump_only=True, only=['id', 'title'])
    answer = fields.Nested(AnswerSchema, attribute="m_answer", dump_only=True, only=['id', 'title'])
    up_votes = fields.Integer(required=True)
    down_votes = fields.Integer(required=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'votes': data}
        return data
