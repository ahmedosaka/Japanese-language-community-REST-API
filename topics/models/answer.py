from extensions import db


class Answer(db.Model):
    __tablename__ = "m_answer"

    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False, index=True, autoincrement=True)
    title = db.Column(db.VARCHAR(50), nullable=False, primary_key=True)
    contents = db.Column(db.VARCHAR(500), nullable=False, primary_key=True)
    published_date = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    author_id = db.Column(db.Integer(), db.ForeignKey("m_user.id"), nullable=True)
    topic_id = db.Column(db.Integer(), db.ForeignKey("t_topics.id"), nullable=True)

    votes = db.relationship("Votes", backref="m_answer")
    @classmethod
    def get_answers_by_topic_id(cls, topic_id):
        return cls.query.filter_by(topic_id=topic_id).all()

    @classmethod
    def get_answer_by_topic_id_and_answer_id(cls, topic_id, id):
        return cls.query.filter_by(topic_id=topic_id).filter_by(id=id).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

