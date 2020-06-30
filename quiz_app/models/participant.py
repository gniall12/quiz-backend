from ..db import db


class ParticipantModel(db.Model):
    """Participant in a quiz.

    Attributes:
        quiz_id: The ID of the quiz the participant is participating in.
        name: The name of the participant.
        score: The participant's score in the quiz.
    """

    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer)
    name = db.Column(db.String(80))
    score = db.Column(db.Integer)

    def __init__(self, quiz_id, name, score=0):
        """ Inits the ParticipantModel."""
        self.quiz_id = quiz_id
        self.name = name
        self.score = score

    def json(self):
        """Converts the ParticipantModel to JSON."""
        return {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "name": self.name,
            "score": self.score,
        }

    @classmethod
    def find_by_id(cls, id):
        """Finds a participant by their ID."""
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all_by_quiz_id(cls, quiz_id):
        """Finds all participants for a quiz.

        Args:
            quiz_id: the ID of the quiz to find participants for.

        Returns:
            A list of ParticipantModel objects.
        """

        return cls.query.filter_by(quiz_id=quiz_id).all()

    def save_to_db(self):
        """Saves ParticipantModel object to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes ParticipantModel object from the database."""
        db.session.delete(self)
        db.session.commit()
