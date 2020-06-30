from ..db import db


class QuestionModel(db.Model):
    """Question in a quiz.

    Attributes:
        quiz_id: The ID of the quiz the question is in.
        round_number: The round of the quiz the question is in.
        question: The text of the question.
    """

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer)
    round_number = db.Column(db.Integer)
    question = db.Column(db.String(80))

    def __init__(self, quiz_id, round_number, question):
        """ Inits the QuestionModel."""
        self.quiz_id = quiz_id
        self.round_number = round_number
        self.question = question

    def json(self):
        """Converts the QuestionModel to JSON."""
        return {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "round_number": self.round_number,
            "question": self.question,
        }

    @classmethod
    def find_quiz_questions(cls, quiz_id):
        """Finds all questions for a quiz.

        Args:
            quiz_id: the ID of the quiz to find questions for.

        Returns:
            A list of QuestionModel objects.
        """
        return cls.query.filter_by(quiz_id=quiz_id).all()

    @classmethod
    def find_round_questions(cls, quiz_id, round_number):
        """Finds all questions for a round of a quiz.

        Args:
            quiz_id: the ID of the quiz to find questions for.
            quiz_id: the number of the round to find questions for.

        Returns:
            A list of QuestionModel objects.
        """
        return cls.query.filter_by(quiz_id=quiz_id, round_number=round_number).all()

    def save_to_db(self):
        """Saves QuestionModel object to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes QuestionModel object from the database."""
        db.session.delete(self)
        db.session.commit()
