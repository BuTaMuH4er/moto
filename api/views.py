from flask_restful import Resource
from flask import render_template
from api.model import db, Motocycle

class ProductAPI(Resource):

    def get(self):
        motocycle = Motocycle.query.order_by(Motocycle.brand_name.desc()).all()
        return render_template('index.html',motocycle=motocycle)

