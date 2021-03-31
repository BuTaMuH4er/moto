from flask_restful import Api
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api import views
from flask_migrate import Migrate


migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db = SQLAlchemy(app)
    api = Api(app)
    db.init_app(app)
    migrate.init_app(app, db)
    #api.add_resource(views.motocycles_API, '/<string:id>')
    api.add_resource(views.cycle_by_id, '/by_id/<int:id>')
    return app