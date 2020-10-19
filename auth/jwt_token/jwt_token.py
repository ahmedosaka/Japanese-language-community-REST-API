# -*- coding: utf-8 -*-
import os
import uuid
from datetime import datetime, timedelta
import jwt


class Config(object):
    # Header
    ALGORITHM = 'HS256'
    # Payload
    EXPIRATION_DELTA = timedelta(days=1)
    # Others
    SECRET_KEY = os.urandom(32)


class JWTError(Exception):
    pass



class JWTToken(object):
    @staticmethod
    def encode(identity):
        headers = {
            'alg': Config.ALGORITHM,
        }
        now = datetime.utcnow()
        exp = now + Config.EXPIRATION_DELTA
        payload = {
            'exp': exp,
            'nbf': now,
            'iat': now,
            'identity': identity,
            'jti': str(uuid.uuid4()),
        }
        token = jwt.encode(
            payload,
            Config.SECRET_KEY,
            algorithm=Config.ALGORITHM,
            headers=headers)
        token = token.decode('UTF-8')
        exp = exp.isoformat()
        return token, exp

    @staticmethod
    def decode(token):
        try:
            payload = jwt.decode(
                token,
                Config.SECRET_KEY,
                algorithm=Config.ALGORITHM)
        except Exception as e:
            raise JWTError('Authorization failed.', e)
        return payload
