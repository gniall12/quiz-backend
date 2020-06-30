from flask_restful import Resource, reqparse

from ..models.participant import ParticipantModel
from ..models.quiz import QuizModel


class Participant(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("quiz_id", type=str, required=True)
    parser.add_argument("name", type=str, required=True)

    def post(self):
        """Adds a participant to a quiz.

        Quiz id and participant name should be specified in the request body.

        Returns:
            The participant added in JSON form.
        """
        data = Participant.parser.parse_args()
        participant_obj = ParticipantModel(data["quiz_id"], data["name"])

        quiz_obj = QuizModel.find_by_id(data["quiz_id"])

        if not quiz_obj:
            return {"message": "Quiz not found"}, 404
        if quiz_obj.current_round is not None:
            return {"message": "Quiz has already started"}, 403

        try:
            participant_obj.save_to_db()
        except:
            return {"message": "An error occurred inserting the participant."}

        return participant_obj.json()

    def delete(self, id):
        """Deletes a participant from a quiz.

        Args:
            id: the ID of the participant to be deleted.

        Returns:
            A JSON message confirming that the participant is deleted.
        """
        participant_obj = ParticipantModel.find_by_id(id)

        if participant_obj:
            try:
                participant_obj.delete_from_db()
            except:
                return {"message": "An error occurred deleting the participant"}
            return {"message": "Participant deleted."}

        return {"message": "Participant not found"}, 404


class Participants(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("participants", type=dict, action="append", required=True)

    def get(self, quiz_id):
        """Gets a list of participants in a quiz.

        Args:
            quiz_id: the ID of the quiz.

        Returns:
            A list of participants in JSON form.
        """
        participant_obj_list = ParticipantModel.find_all_by_quiz_id(quiz_id)

        if participant_obj_list:
            return {
                "participants": [
                    participant_obj.json() for participant_obj in participant_obj_list
                ]
            }

        return {"message": "Quiz not found"}, 404

    def put(self, quiz_id):
        """Updates a list of participants in a quiz.

        Request body should contain participant objects with updated scores.

        Args:
            quiz_id: the ID of the quiz.

        Returns:
            A list of updated participants in JSON form.
        """
        data = Participants.parser.parse_args()
        participants = data["participants"]
        updated_participant_obj_list = []

        for participant in participants:
            participant_obj = ParticipantModel.find_by_id(participant["id"])
            if participant_obj:
                participant_obj.score = participant["score"]
                participant_obj.save_to_db()
                updated_participant_obj_list.append(participant_obj)

        return {
            "participants": [
                updated_participant_obj.json()
                for updated_participant_obj in updated_participant_obj_list
            ]
        }
