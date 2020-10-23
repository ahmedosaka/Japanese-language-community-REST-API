from flask import request
from flask_restful import Resource
from http import HTTPStatus
import json

from auth.jwt_token.jwt_token import JWTToken
from topics.schemas.topics import TopicSchema
from topics.models.topics import Topic
from auth.resources.token import TokenResource, login_required, record_author
from auth.models.user import User
from base.exceptions import MyBadRequestException, MyInternalServerErrorException

topic_schema = TopicSchema()
topic_list_schema = TopicSchema(many=True)
token_resource = TokenResource()
JWTToken = JWTToken()

japanese_levels = ["general", "N1", "N2", "N3", "N4", "N5"]


class TopicViews(Resource):

    @login_required
    def get(self, username):
        try:
            topic_data = Topic.get_all_topics()
        except Exception as e:
            MyInternalServerErrorException

        return topic_list_schema.dump(topic_data).data, HTTPStatus.OK


    @login_required
    def post(self, username):

        user = record_author()
        try:
            json_data = request.get_json()
            for i in range(7):
                if i == json_data["japanese_level"]:
                    json_data["japanese_level"] = japanese_levels[i]
        except Exception as e:
            raise MyBadRequestException
        data, errors = topic_schema.load(data=json_data)
        if errors:
            raise MyBadRequestException
        topic = Topic(**data)
        topic.author_id = user.id

        topic.save()

        return topic_schema.dump(topic).data, HTTPStatus.CREATED
