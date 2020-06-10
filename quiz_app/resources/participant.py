from flask_restful import Resource, reqparse

from ..models.participant import ParticipantModel
from ..models.quiz import QuizModel


class Participant(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True)

    def post(self, quiz_id):
        data = Participant.parser.parse_args()
        participant_obj = ParticipantModel(quiz_id, data["name"])

        quiz_obj = QuizModel.find_by_id(quiz_id)

        if not quiz_obj:
            return {"message": "Quiz not found"}, 404
        if quiz_obj.current_round is not None:
            return {"message": "Quiz has already started"}, 403

        try:
            participant_obj.save_to_db()
        except:
            return {"message": "An error occurred inserting the participant."}

        return participant_obj.json()


class Participants(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("participants", type=dict, action="append", required=True)

    def get(self, quiz_id):
        participant_obj_list = ParticipantModel.find_all_by_quiz_id(quiz_id)

        if participant_obj_list:
            return {
                "participants": [
                    participant_obj.json() for participant_obj in participant_obj_list
                ]
            }

        return {"message": "Quiz not found"}, 404

    def put(self, quiz_id):
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
