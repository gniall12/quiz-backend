from flask_restful import Resource, reqparse
from flask import Response
from flask.helpers import url_for
from flask_sse import sse


class Change(Resource):
    def get(self, quiz_id):
        """Publishes message to client to notify them of a change in quiz state.

        Used to let client know when the quizmaster has progressed to the 
        next stage or round of the quiz.

        Args:
            quiz_id: The ID of the quiz that is progressing.

        Returns:
            The quiz ID of the quiz that is progressing.
        """
        sse.publish({"message": "Hello!"}, channel=quiz_id)
        return quiz_id
