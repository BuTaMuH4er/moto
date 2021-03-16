from flask_restful import Api
from flask import Flask
from api.model import db
import api.views as views
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    api = Api(app)
    db.init_app(app)
    api.add_resource(views.ProductAPI, '/')
    return app