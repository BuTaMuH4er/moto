from flask_restful import Resource, reqparse
from api.model import db, Motocycle
import json





class motocycles_API(Resource):

    def get(self, id=None):
        motocycle = Motocycle.query.order_by(Motocycle.brand_name.desc()).all()
        return [moto.to_dict() for moto in motocycle]


class cycle_by_id(Resource):

    def get(self, id):
        if isinstance(id, int):
            count_vehicles = Motocycle.query.filter_by(id=id).count()
            if count_vehicles:
                motocycle = Motocycle.query.filter_by(id=id).first()
                return motocycle.to_dict()
            return {'error':'There is no motocycle, wrong id.'}
        return {'error':'Wrong format "id"'}


