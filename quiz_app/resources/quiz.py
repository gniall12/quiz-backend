from flask_restful import Resource, reqparse
from flask_sse import sse

from ..models.quiz import QuizModel


class Quiz(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank!"
    )
    put_parser = reqparse.RequestParser()
    put_parser.add_argument("current_round", type=int, required=False)
    put_parser.add_argument("number_rounds", type=int, required=False)
    put_parser.add_argument("current_page", type=str, required=False)

    def get(self, id):
        """Gets a quiz.

        Args:
            id: the ID of the quiz.

        Returns:
            A quiz in JSON form.
        """
        quiz_obj = QuizModel.find_by_id(id)
        if quiz_obj:
            return quiz_obj.json()
        return {"message": "Quiz not found"}, 404

    def post(self):
        """Adds a quiz to the database.

        Quiz name should be specified in the request body.
        """
        data = Quiz.post_parser.parse_args()
        quiz_obj = QuizModel(data["name"])

        try:
            quiz_obj.save_to_db()
        except:
            return {"message": "An error occurred inserting the quiz."}

        return quiz_obj.json()

    def put(self, id):
        """Updates a quiz's current round and/or number of rounds.

        New current round and/or number of rounds value should be specified 
        in the request body.

        Attributes:
            id: The ID of the quiz to update.

        Returns:
            The updated quiz in JSON form.
        """
        quiz_obj = QuizModel.find_by_id(id)
        data = Quiz.put_parser.parse_args()
        if quiz_obj:
            if data["current_round"] is not None:
                quiz_obj.current_round = data["current_round"]
            if data["number_rounds"] is not None:
                quiz_obj.number_rounds = data["number_rounds"]
            if data["current_page"] is not None:
                quiz_obj.current_page = data["current_page"]
            quiz_obj.save_to_db()
        else:
            return {"message": "Quiz not found"}, 404
        sse.publish(quiz_obj.json(), channel=id)

        return quiz_obj.json()

    def delete(self, id):
        """Deletes a quiz.

        Args:
            id: the ID of the quiz to be deleted.

        Returns:
            A JSON message confirming that the quiz is deleted.
        """
        quiz_obj = QuizModel.find_by_id(id)

        if quiz_obj:
            quiz_obj.delete_from_db()
            return {"message": "Quiz deleted"}
        return {"message": "Quiz not found"}, 404
