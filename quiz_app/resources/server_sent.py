from flask_restful import Resource, reqparse
from flask import Response

changed_quiz_id = 0


class ChangeStream(Resource):
    def get(self, quiz_id):
        def eventStream(quiz_id):
            global changed_quiz_id
            while True:
                if changed_quiz_id == quiz_id:
                    yield f"data: {changed_quiz_id}\n\n"
                    changed_quiz_id = 0

        return Response(eventStream(quiz_id), mimetype="text/event-stream")


class Change(Resource):
    def get(self, quiz_id):
        global changed_quiz_id
        changed_quiz_id = quiz_id
        return quiz_id
