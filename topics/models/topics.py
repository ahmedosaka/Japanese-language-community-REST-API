from extensions import db
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy import desc
from auth.models.user import User


class Topic(db.Model):
    __tablename__ = 't_topics'

    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False, index=True, autoincrement=True)
    title = db.Column(db.VARCHAR(50), nullable=False, index=True, primary_key=True)
    contents = db.Column(db.VARCHAR(500), nullable=False, index=True, primary_key=True)
    japanese_level = db.Column(db.VARCHAR(50), nullable=False)
    published_date = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    author_id = db.Column(db.Integer(), db.ForeignKey("m_user.id"), nullable=True)

    answers = db.relationship("Answer", backref='t_topics')
    votes = db.relationship("Votes", backref="t_topics")


    @classmethod
    def get_all_topics(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_topic_id(cls, topic_id):
        return cls.query.filter_by(id=topic_id).first()

    @classmethod
    def get_all_topics(cls):
        return cls.query.all()
