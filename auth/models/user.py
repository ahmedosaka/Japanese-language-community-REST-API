from extensions import db


class User(db.Model):
    __tablename__ = "m_user"
    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False, index=True, autoincrement=True)  # ID
    username = db.Column(db.VARCHAR(255), nullable=False, unique=True, index=True)  # ユーザー名
    password = db.Column(db.VARCHAR(200), nullable=False)  # パスワード
    first_name = db.Column(db.VARCHAR(255), nullable=False)
    last_name = db.Column(db.VARCHAR(255), nullable=False)
    created = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())  # 登録した日時
    modified = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())  # 更新した日時

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
