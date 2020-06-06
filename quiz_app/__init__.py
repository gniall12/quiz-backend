from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from .db import db

from .config import AppConfig, frontend_url
from .resources.quiz import Quiz
from .resources.question import Questions
from .resources.participant import Participant, Participants
from .resources.answer import Answers
from .resources.server_sent import ChangeStream, Change


def create_app():
    app = Flask(__name__)
    app.config.from_object("quiz_app.config.AppConfig")
    
    CORS(app)

    api = Api(app)

    api.add_resource(Quiz, "/quiz", "/quiz/<string:id>")
    api.add_resource(
        Questions,
        "/questions/<string:quiz_id>",
        "/questions/<string:quiz_id>/<int:round_number>",
    )
    api.add_resource(Participant, "/participant/<string:quiz_id>")
    api.add_resource(Participants, "/participants/<string:quiz_id>")
    api.add_resource(
        Answers,
        "/answers",
        "/answers/<string:quiz_id>",
        "/answers/<string:quiz_id>/<int:round_num>",
        "/answers/<string:quiz_id>/<int:round_num>/<int:participant_id>",
    )
    api.add_resource(ChangeStream, "/change-stream/<string:quiz_id>")
    api.add_resource(Change, "/change/<string:quiz_id>")

    @app.before_first_request
    def create_tables():
        db.create_all()

    db.init_app(app)

    return app
