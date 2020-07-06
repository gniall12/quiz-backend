from ..db import db
from .question import QuestionModel


class AnswerModel(db.Model):
    """Answer to a quiz question.

    Attributes:
        question_id: The ID of the question answered.
        participant_id: The ID of the participant who answered.
        answer: The text of the answer to the question
        question: The question object, instance of QuestionModel class
    """

    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    participant_id = db.Column(db.Integer)
    answer = db.Column(db.String(80))
    question = db.relationship(
        "QuestionModel", backref=db.backref("questions", uselist=False)
    )

    def __init__(self, question_id, participant_id, answer):
        """Inits the AnswerModel"""
        self.question_id = question_id
        self.participant_id = participant_id
        self.answer = answer

    def json(self):
        """Converts the AnswerModel to JSON"""
        return {
            "id": self.id,
            "question_id": self.question_id,
            "participant_id": self.participant_id,
            "answer": self.answer,
            "question": self.question.question,
        }

    @classmethod
    def find_participant_answers(
        cls, quiz_id=None, round_num=None, participant_id=None
    ):
        """Gets answers for a given quiz, round, or participant from the database.

        The optional parameters dictate which answers we want retrieved. If no
        parameters are supplied, all answers will be retrieved. If a quiz ID 
        is supplied, all answers for that quiz will be retrieved. And so on.

        Args:
            quiz_id: Optional parameter. Specifies the quiz to return answers 
                from.
            round_num: Optional parameter. Specifies the round number to 
                return answers from.
            participant_id: Optional parameter. Specifies the participant to 
                return answers for.

        Returns:
            A list of AnswerModel objects.
        """
        query = cls.query.join(QuestionModel)
        if quiz_id is not None:
            query = query.filter(QuestionModel.quiz_id == quiz_id)
            if round_num is not None:
                query = query.filter(QuestionModel.round_number == round_num)
                if participant_id is not None:
                    query = query.filter(cls.participant_id == participant_id)
        return query.all()

    def save_to_db(self):
        """Saves AnswerModel object to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes AnswerModel object from the database"""
        db.session.delete(self)
        db.session.commit()
