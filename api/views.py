from flask_restful import Resource, reqparse
from api.model import Motocycle, BrandsMotocycle
from sqlalchemy import and_
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
            abort(404)
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


class list_brands(Resource):

    def get(self):
        brands = dict()
        list_brands = BrandsMotocycle.query.all()
        for i in list_brands:
            brands[i.brand_name] = i.id
        return brands


class show_by_brand(Resource):

    def get(self, id_brand):
        if isinstance(id_brand, list):
            list_motos = Motocycle.query.filter_by(brand_name=(id_brand)).all()
            result = dict()
            for moto in list_motos:
                result[moto.id] = {
                    'brand_name': moto.brands.brand_name,
                    'model': moto.model,
                    'engine': moto.engine
                }
            return result
        list_motos = Motocycle.query.filter_by(brand_name=id_brand).all()
        result = dict()
        for moto in list_motos:
            result[moto.id] = {
                'brand_name': moto.brands.brand_name,
                'model': moto.model,
                'engine': moto.engine
            }
        return result


class show_by_gear(Resource):

    def get(self, gear):
        result = dict()
        list_motos = Motocycle.query.filter_by(gear_type=gear).all()
        for moto in list_motos:
            result[moto.id] = {
                'brand_name':moto.brands.brand_name,
                'model':moto.model,
                'gear_type':gear
            }
        return result


class show_by_engine(Resource):

    def get(self, size):
        result = dict()
        if size == '125':
            list_motocycles = Motocycle.query.filter(Motocycle.engine <= int(size)).all()
        if size == '400':
            list_motocycles = Motocycle.query.filter(and_(Motocycle.engine > 125, Motocycle.engine <= 400)).all()
        if size == '999':
            list_motocycles = Motocycle.query.filter(and_(Motocycle.engine > 400, Motocycle.engine <= 999)).all()
        if size == 'liter':
            list_motocycles = Motocycle.query.filter(Motocycle.engine > 999).all()
        for moto in list_motocycles:
            motocycle = Motocycle.query.filter_by(id=moto.id).first()
            result[motocycle.id] = {
                'brand_name': motocycle.brands.brand_name,
                'model': motocycle.model,
                'engine': motocycle.engine
            }
        return result


class show_by_engine_type(Resource):

    def get(self, engine_type):
        result = dict()
        list_motocycles = Motocycle.query.filter(Motocycle.type_engine == engine_type).all()
        for moto in list_motocycles:
            motocycle = Motocycle.query.filter_by(id=moto.id).first()
            result[motocycle.id] = {
                'brand_name': motocycle.brands.brand_name,
                'model': motocycle.model,
                'engine_type': motocycle.type_engine
            }
        return result


class show_by_class_motocycle(Resource):

    def get(self, moto_class):
        result = dict()
        list_motocycle_class = Motocycle.query.filter(Motocycle.cycle_class == moto_class).all()
        print(list_motocycle_class)
        for moto in list_motocycle_class:
            motocycle = Motocycle.query.filter_by(id=moto.id).first()
            result[motocycle.id] = {
                'brand_name' : motocycle.brands.brand_name,
                'model' : motocycle.model,
                'motocycle_class' : motocycle.cycle_class
            }
        return result