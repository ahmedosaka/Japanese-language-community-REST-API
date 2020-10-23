from flask import request
from flask_restful import Resource
from http import HTTPStatus

from auth.resources.token import login_required, record_author
from topics.models.answer import Answer
from base.exceptions import MyInternalServerErrorException, MyBadRequestException
from topics.schemas.answer import AnswerSchema
from topics.models.topics import Topic
from topics.schemas.topics import TopicSchema
from topics.models.votes import Votes
from topics.schemas.votes import VotesSchema

TopicSchema = TopicSchema()
answer_list_schema = AnswerSchema(many=True)
answer_schema = AnswerSchema()
votes_schema = VotesSchema()


# in this view, you will be getting all the answers of specific topic by the topic id.
# /topics/<topic_id>/answers
class AnswerViews_by_topic_ID(Resource):

    @login_required
    def get(self, username, topic_id):

        try:
            topic_data = Topic.get_by_topic_id(topic_id=topic_id)
            answer_data = Answer.get_answers_by_topic_id(topic_id=topic_id)
        except Exception as e:
            return MyInternalServerErrorException
        topic_dumped_data = TopicSchema.dump(topic_data).data
        answer_dumped_data = answer_list_schema.dump(answer_data).data
        topic_dumped_data.update(answer_dumped_data)

        return topic_dumped_data, HTTPStatus.OK

    @login_required
    def post(self, username, topic_id):
        user = record_author()
        try:
            json_data = request.get_json()
        except Exception as e:
            raise MyBadRequestException

        data, errors = answer_schema.load(data=json_data)
        if errors:
            raise MyBadRequestException
        answer = Answer(**data)
        answer.author_id = user.id
        answer.topic_id = topic_id

        try:
            answer.save()
        except Exception as e:
            MyInternalServerErrorException

        return answer_schema.dump(answer).data, HTTPStatus.CREATED


# /topics/<topic_id>/answers/<answer_id>
class AnswerView_byTopicID_AnswerID(Resource):

    @login_required
    def get(self, username, topic_id, answer_id):
        answer_by_id = Answer.get_answer_by_topic_id_and_answer_id(topic_id=topic_id, id=answer_id)
        return answer_schema.dump(answer_by_id).data, HTTPStatus.OK

    @login_required
    def put(self, username, topic_id, answer_id):
        json_data = request.get_json()

        data, errors = answer_schema.load(json_data)

        try:
            answer_by_id = Answer.get_answer_by_topic_id_and_answer_id(topic_id=topic_id, id=answer_id)
        except Exception as e:
            raise MyInternalServerErrorException

        answer_by_id.title = data.get("title") or answer_by_id.title
        answer_by_id.contents = data.get("contents") or answer_by_id.contents

        try:
            answer_by_id.save()
        except Exception as e:
            raise MyInternalServerErrorException
        try:
            answer_by_id = Answer.get_answer_by_topic_id_and_answer_id(topic_id=topic_id, id=answer_id)
        except Exception as e:
            raise MyInternalServerErrorException

        return answer_schema.dump(answer_by_id).data, HTTPStatus.OK

    @login_required
    def delete(self, username, topic_id, answer_id):
        try:
            answer_by_id = Answer.get_answer_by_topic_id_and_answer_id(topic_id=topic_id, id=answer_id)
        except Exception as e:
            raise MyInternalServerErrorException
        if answer_by_id is None:
            raise MyBadRequestException
        try:
            answer_by_id.delete()
        except Exception as e:
            MyInternalServerErrorException

        return {}, HTTPStatus.NOT_FOUND


# /topics/<topic_id>/answers/<answer_id>/votes
class vote_answer_by_id(Resource):
    @login_required
    def put(self, username, topic_id, answer_id):
        user = record_author()
        try:
            json_data = request.get_json()
        except Exception as e:
            raise MyBadRequestException
        data, errors = votes_schema.load(json_data)

        try:
            answer_by_id = Answer.get_answer_by_topic_id_and_answer_id(topic_id=topic_id, id=answer_id)
        except Exception as e:
            raise MyInternalServerErrorException

        up_votes = data.get("up_votes")
        down_votes = data.get("down_votes")
        check_user_if_voted = Votes.check_author_if_voted(author_id=user.id, topic_id=topic_id, answer_id=answer_id)

        if check_user_if_voted:
            if up_votes == 0 and down_votes ==0:
                check_user_if_voted.delete()
                return {}, HTTPStatus.OK
            else:
                raise MyBadRequestException
        elif check_user_if_voted is None:
            if up_votes == 0 and down_votes == 0:
                return {}, HTTPStatus.OK
            if up_votes == 1 or up_votes == 0:
                if down_votes == 1 or down_votes == 0:
                    if down_votes == 1 and up_votes == 1:
                        raise MyBadRequestException
                    else:
                        vote_data = {}
                        data, errors = votes_schema.load(vote_data)
                        vote = Votes(**data)
                        vote.answer_id = answer_id
                        vote.topic_id = topic_id
                        vote.author_id = user.id
                        vote.up_votes = up_votes
                        vote.down_votes = down_votes
                else:
                    raise MyBadRequestException
            else:
                raise MyBadRequestException
        try:
            vote.save()
        except Exception as e:
            raise MyInternalServerErrorException

        return votes_schema.dump(vote).data, HTTPStatus.OK
