import datetime
from sqlalchemy import DateTime

from ..db import db


class QuizModel(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(DateTime, default=datetime.datetime.utcnow)
    name = db.Column(db.String(80))
    number_rounds = db.Column(db.Integer)
    current_round = db.Column(db.Integer)

    def __init__(self, name, number_rounds=None, current_round=None):
        self.name = name
        self.number_rounds = number_rounds
        self.current_round = current_round

    def json(self):
        return {
            "id": self.id,
            "date_created": str(self.date_created),
            "name": self.name,
            "number_rounds": self.number_rounds,
            "current_round": self.current_round,
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
