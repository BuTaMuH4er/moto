from flask_restful import Resource
from api.model import db, Motocycle
import json





class motocycles_API(Resource):
    def get(self):
        motocycle = Motocycle.query.order_by(Motocycle.brand_name.desc()).all()
        return [moto.to_dict() for moto in motocycle]


