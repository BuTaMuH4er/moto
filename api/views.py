from flask_restful import Resource
from api.model import db, Motocycle
import json





class ProductAPI(Resource):
    def get(self):
        dict_cycles = []
        motocycle = Motocycle.query.order_by(Motocycle.brand_name.desc()).all()
        for moto in motocycle:
            dict_cycles.append(moto.to_dict())
        return dict_cycles


