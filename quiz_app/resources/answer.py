from flask_restful import Resource, reqparse

from ..models.answer import AnswerModel


class Answers(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("answers", type=dict, action="append", required=True)

    def get(self, quiz_id=None, round_num=None, participant_id=None):
        answers = AnswerModel.find_participant_answers(
            quiz_id, round_num, participant_id
        )
        if answers:
            return {"answers": [answer.json() for answer in answers]}
        return {"message": "answers not found"}, 404

    def post(self):
        data = Answers.parser.parse_args()
        answers = data["answers"]

        answer_obj_list = []

        for answer in answers:
            answer_obj = AnswerModel(
                answer["question_id"], answer["participant_id"], answer["answer"],
            )
            answer_obj_list.append(answer_obj)

        try:
            for answer_obj in answer_obj_list:
                answer_obj.save_to_db()
        except:
            return {"message": "An error occurred inserting the answers."}

        return {"answers": [answer_obj.json() for answer_obj in answer_obj_list]}
