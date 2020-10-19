from werkzeug.exceptions import HTTPException


class MyException(HTTPException):
    code: str  # custom field
    description: str  # custom field

    def __init__(self):
        pass


class MyBadRequestException(MyException):
    code = 400
    description = "パラメータに誤りがあります。"


class MyUnauthorizedException(MyException):
    code = 401
    description = "認証に失敗しました。"


class MyInternalServerErrorException(MyException):
    code = 500
    description = "サーバ内部で異常が発生しました。"
