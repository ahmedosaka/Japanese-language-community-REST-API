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
    is_admin = db.Column(db.BOOLEAN(), nullable=True, default=False)

    topics = db.relationship("Topic", backref="m_user")
    answers = db.relationship("Answer", backref="m_answer")
    votes = db.relationship("Votes", backref="m_user")

    # your_leader_name = db.Column(db.VARCHAR(255), nullable=False, default=None)
    # your_first_student_name = db.Column(db.VARCHAR(255), nullable=False, default=None)
    # your_second_student_name =db.Column(db.VARCHAR(255), nullable=False, default=None)
    # your_third_student_name =db.Column(db.VARCHAR(255), nullable=False, default=None)
    # rank = db.Column(db.Integer(),default=None, nullable=False)
    # points= db.Column(db.VARCHAR(50), default=0, nullable=True)

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
