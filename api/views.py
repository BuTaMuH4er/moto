from flask_restful import Resource, reqparse
from api.model import Motocycle, BrandsMotocycle
from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()


parser = reqparse.RequestParser()
parser.add_argument('brand_name', type=str)
parser.add_argument('model', type=str)
parser.add_argument('engine', type=int)


class motocycles_API(Resource):

    #def get(self, id=None):
    #    motocycle = Motocycle.query.order_by(Motocycle.brand_name.desc()).all()
    #    return [moto.to_dict() for moto in motocycle]

    def get(self, id=None):
        if id is None:
            motocycles = Motocycle.query.all()
        else:
            motocycles = [Motocycle.query.get(id)]
        if not motocycles:
            abort (404)
        result = {}
        for moto in motocycles:
            result[moto.id] = {
                'brand_name':moto.brands.brand_name,
                'model':moto.model,
                'engine':moto.engine
            }
        return result


class cycle_by_id(Resource):

    def get(self, id):
        if isinstance(id, int):
            count_vehicles = Motocycle.query.filter_by(id=id).count()
            if count_vehicles:
                motocycle = Motocycle.query.filter_by(id=id).first()
                return motocycle.to_dict()
            return {'error':'There is no motocycle, wrong id.'}
        return {'error':'Wrong format "id"'}



