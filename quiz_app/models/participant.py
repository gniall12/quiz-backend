from ..db import db


class ParticipantModel(db.Model):
    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer)
    name = db.Column(db.String(80))
    score = db.Column(db.Integer)

    def __init__(self, quiz_id, name, score=0):
        self.quiz_id = quiz_id
        self.name = name
        self.score = score

    def json(self):
        return {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "name": self.name,
            "score": self.score,
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all_by_quiz_id(cls, quiz_id):
        return cls.query.filter_by(quiz_id=quiz_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
