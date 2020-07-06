from flask_restful import Resource, reqparse

from ..models.answer import AnswerModel


class Answers(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("answers", type=dict, action="append", required=True)

    def get(self, quiz_id=None, round_num=None, participant_id=None):
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
            A list of answers in JSON form.
        """
        answers = AnswerModel.find_participant_answers(
            quiz_id, round_num, participant_id
        )
        if answers:
            return {"answers": [answer.json() for answer in answers]}
        return {"message": "answers not found"}, 404

    def post(self):
        """Adds a list of answers to the database.

        Answers to be added are contained in the request body.

        Returns:
            The list of answers added in JSON form
        """
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
