from extensions import db


class Votes(db.Model):
    __tablename__ = "m_votes"

    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False, index=True, autoincrement=True)
    author_id = db.Column(db.Integer(), db.ForeignKey("m_user.id"), nullable=False)
    topic_id = db.Column(db.Integer(), db.ForeignKey("t_topics.id"), nullable=False)
    answer_id = db.Column(db.Integer(), db.ForeignKey("m_answer.id"), nullable=False)
    up_votes = db.Column(db.Integer(), nullable=True, default=0)
    down_votes = db.Column(db.Integer(), nullable=True, default=0)

    @classmethod
    def check_author_if_voted(cls, author_id, topic_id, answer_id):
        return cls.query.filter_by(author_id=author_id).filter_by(topic_id=topic_id).filter_by(answer_id= answer_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()