from ..db import db


class QuestionModel(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer)
    round_number = db.Column(db.Integer)
    question = db.Column(db.String(80))

    def __init__(self, quiz_id, round_number, question):
        self.quiz_id = quiz_id
        self.round_number = round_number
        self.question = question

    def json(self):
        return {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "round_number": self.round_number,
            "question": self.question,
        }

    @classmethod
    def find_quiz_questions(cls, quiz_id):
        return cls.query.filter_by(quiz_id=quiz_id).all()

    @classmethod
    def find_round_questions(cls, quiz_id, round_number):
        return cls.query.filter_by(quiz_id=quiz_id, round_number=round_number).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
