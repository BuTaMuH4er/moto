from flask_restful import Api
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api import views
from flask_migrate import Migrate




def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db = SQLAlchemy(app)
    api = Api(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    api.add_resource(views.motocycles_API, '/<int:id>', '/')
    api.add_resource(views.cycle_by_id, '/by_id/<int:id>')
    api.add_resource(views.list_brands, '/brands')
    api.add_resource(views.show_by_brand, '/by_brand/<int:id_brand>')
    api.add_resource(views.show_by_gear, '/by_gear_type/<string:gear>')
    return app