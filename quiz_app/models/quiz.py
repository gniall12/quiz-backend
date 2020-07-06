import datetime
from sqlalchemy import DateTime

from ..db import db


class QuizModel(db.Model):
    """Quiz.

    Attributes:
        date_created: The date/time on which the quiz was created.
        name: The name of the quiz.
        number_rounds: The number of rounds in the quiz.
        current_round: The round which the quiz is currently at.
        current_page: The current stage of the quiz, controlled by the quizmaster.
    """

    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(DateTime, default=datetime.datetime.utcnow)
    name = db.Column(db.String(80))
    number_rounds = db.Column(db.Integer)
    current_round = db.Column(db.Integer)
    current_page = db.Column(db.String(80))

    def __init__(self, name, number_rounds=None, current_round=None):
        """ Inits the QuizModel."""
        self.name = name
        self.number_rounds = number_rounds
        self.current_round = current_round

    def json(self):
        """Converts the QuizModel to JSON."""
        return {
            "id": self.id,
            "date_created": str(self.date_created),
            "name": self.name,
            "number_rounds": self.number_rounds,
            "current_round": self.current_round,
            "current_page": self.current_page,
        }

    @classmethod
    def find_by_id(cls, id):
        """Finds a participant by their ID."""
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        """Saves QuizModel object to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes QuizModel object from the database."""
        db.session.delete(self)
        db.session.commit()
