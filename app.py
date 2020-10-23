from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from auth.resources.user import UserView
from auth.resources.token import TokenResource
from topics.resources.topics import TopicViews
from topics.resources.answer import AnswerViews_by_topic_ID, AnswerView_byTopicID_AnswerID, vote_answer_by_id

from config import Config
from extensions import db
from base.exceptions import MyException


class MyApi(Api):
    def handle_error(self, e: MyException):
        if isinstance(e, MyException):
            return self.make_response({
                'code': str(e.code),
                'description': e.description,
            }, e.code)
        else:
            return super().handle_error(e)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)

    register_resources(app)

    return app


def register_extensions(app):
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


def register_resources(app):
    api = MyApi(app)

    api.add_resource(UserView, '/users')
    api.add_resource(TokenResource, '/api/v1/auth/login')
    api.add_resource(TopicViews, '/api/v1/topics')
    api.add_resource(AnswerViews_by_topic_ID, '/api/topics/<int:topic_id>/answers')
    api.add_resource(AnswerView_byTopicID_AnswerID, '/api/topics/<int:topic_id>/answers/<int:answer_id>')
    api.add_resource(vote_answer_by_id, "/api/topics/<topic_id>/answers/<answer_id>/votes")


if __name__ == '__main__':
    app = create_app()
    app.run()
