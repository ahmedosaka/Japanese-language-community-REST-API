from http import HTTPStatus
from flask import request
from flask_restful import Resource
import functools

from auth.jwt_token.jwt_token import JWTToken, JWTError
from auth.models.user import User
from utils import check_password
from base.exceptions import MyInternalServerErrorException, MyUnauthorizedException, MyBadRequestException
JWTToken = JWTToken()
JWTError = JWTError()


class TokenResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        except Exception as e:
            raise MyBadRequestException
        try:
            user = User.get_by_username(username=username)
        except Exception as e:
            raise MyInternalServerErrorException
        if user is None or not user or not check_password(password, user.password):
            raise MyBadRequestException
        try:
            token, exp = JWTToken.encode(user.username)
            result = {'access_token': token, 'expire_date': exp}
            return {'result': result}, HTTPStatus.CREATED
        except Exception as e:
            raise MyInternalServerErrorException


def login_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        header = request.headers.get('Authorization')
        _, token = header.split()
        try:
            data = JWTToken.decode(token)
            username = data["identity"]
        except Exception as e:
            raise MyUnauthorizedException
        return f(username, *args, **kwargs)
    return wrapper
