from flask_restful import Api
from flask import Flask
from api.model import db
import api.views as views


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    api = Api(app)
    db.init_app(app)
    api.add_resource(views.ProductAPI, '/')
    return app