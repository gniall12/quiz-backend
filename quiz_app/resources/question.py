from flask_restful import Resource, reqparse

from ..models.question import QuestionModel


class Questions(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("questions", type=dict, action="append", required=True)

    def post(self, quiz_id):
        root_data = Questions.parser.parse_args()

        question_obj_list = []

        for round in root_data["questions"]:
            round_number = round["round_number"]
            for question_text in round["questions"]:
                question_obj = QuestionModel(quiz_id, round_number, question_text)
                question_obj_list.append(question_obj)

        try:
            for question_obj in question_obj_list:
                question_obj.save_to_db()
        except:
            return {"message": "An error occurred inserting the questions."}

        return {
            "questions": [question_obj.json() for question_obj in question_obj_list]
        }

    def get(self, quiz_id, round_number=None):
        if round_number is not None:
            question_obj_list = QuestionModel.find_round_questions(
                quiz_id, round_number
            )
        else:
            question_obj_list = QuestionModel.find_quiz_questions(quiz_id)

        if question_obj_list:
            return {
                "questions": [question_obj.json() for question_obj in question_obj_list]
            }

        return {"message": "Questions not found"}, 404
