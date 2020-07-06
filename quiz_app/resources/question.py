from flask_restful import Resource, reqparse

from ..models.question import QuestionModel


class Questions(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("questions", type=dict, action="append", required=True)

    def post(self, quiz_id):
        """Adds a list of questions to a quiz.

        Questions should be specified in the request body.

        Attributes:
            quiz_id: The ID of the quiz to add the questions to.

        Returns:
            A list of the questions added in JSON form.
        """
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
        """Gets a list of questions in a quiz or round of a quiz.

        If round_number is not specified, all questions for the quiz are returned

        Args:
            quiz_id: the ID of the quiz.
            round_num: Optional parameter. Specifies the round number to 
                return questions from.

        Returns:
            A list of questions in JSON form.
        """
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
