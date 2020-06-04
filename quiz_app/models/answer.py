from ..db import db
from .question import QuestionModel


class AnswerModel(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    participant_id = db.Column(db.Integer)
    answer = db.Column(db.String(80))
    question = db.relationship(
        "QuestionModel", backref=db.backref("questions", uselist=False)
    )

    def __init__(self, question_id, participant_id, answer):
        self.question_id = question_id
        self.participant_id = participant_id
        self.answer = answer

    def json(self):
        return {
            "id": self.id,
            "question_id": self.question_id,
            "participant_id": self.participant_id,
            "answer": self.answer,
            "question": self.question.question,
        }

    @classmethod
    def find_participant_answers(cls, quiz_id=None, round_num=None, participant_id=None):
        query = cls.query.join(QuestionModel)
        if quiz_id is not None:
            query = query.filter(QuestionModel.quiz_id == quiz_id)
            if round_num is not None:
                query = query.filter(QuestionModel.round_number == round_num)
                if participant_id is not None:
                    query = query.filter(cls.participant_id == participant_id)
        return query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
