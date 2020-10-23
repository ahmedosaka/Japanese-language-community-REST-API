from flask import request
from flask_restful import Resource
from http import HTTPStatus
from base.exceptions import MyInternalServerErrorException, MyUnauthorizedException, MyBadRequestException

from auth.models.user import User
from auth.schemas.user import UserSchema

user_schema = UserSchema()


class UserView(Resource):
    def post(self):
        try:
            json_data = request.get_json()
        except Exception as e:
            raise MyBadRequestException
        check_user = False
        try:
            check_user = User.get_by_username(json_data["username"])
        except Exception as e:
            raise MyInternalServerErrorException
        if check_user:
            raise MyBadRequestException

        data, errors = user_schema.load(data=json_data)
        user = User(**data)
        if json_data["is_admin"] == 1:
            user.is_admin = True
        else:
            user.is_admin = False
        try:
            user.save()
        except Exception as e:
            raise MyInternalServerErrorException


        return user_schema.dump(user).data, HTTPStatus.CREATED
