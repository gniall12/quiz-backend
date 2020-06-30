from flask_restful import Resource, reqparse

from ..models.quiz import QuizModel


class Quiz(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank!"
    )
    put_parser = reqparse.RequestParser()
    put_parser.add_argument("current_round", type=int, required=False)
    put_parser.add_argument("number_rounds", type=int, required=False)

    def get(self, id):
        quiz_obj = QuizModel.find_by_id(id)
        if quiz_obj:
            return quiz_obj.json()
        return {"message": "Quiz not found"}, 404

    def post(self):
        data = Quiz.post_parser.parse_args()
        quiz_obj = QuizModel(data["name"])

        try:
            quiz_obj.save_to_db()
        except:
            return {"message": "An error occurred inserting the quiz."}

        return quiz_obj.json()

    def put(self, id):
        quiz_obj = QuizModel.find_by_id(id)
        data = Quiz.put_parser.parse_args()
        if quiz_obj:
            if data["current_round"] is not None:
                quiz_obj.current_round = data["current_round"]
            if data["number_rounds"] is not None:
                quiz_obj.number_rounds = data["number_rounds"]
            quiz_obj.save_to_db()
        else:
            return {"message": "Quiz not found"}, 404

        return quiz_obj.json()

    def delete(self, id):
        quiz_obj = QuizModel.find_by_id(id)

        if quiz_obj:
            quiz_obj.delete_from_db()
            return {"message": "Quiz deleted"}
        return {"message": "Quiz not found"}, 404
