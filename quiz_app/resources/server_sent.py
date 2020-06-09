from flask_restful import Resource, reqparse
from flask import Response
from flask.helpers import url_for
from flask_sse import sse


class Change(Resource):
    def get(self, quiz_id):
        sse.publish({"message": "Hello!"}, channel=quiz_id)
        return quiz_id
