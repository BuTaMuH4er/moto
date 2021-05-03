from flask_sqlalchemy import SQLAlchemy
from api import config
from flask import Flask
from api.model import Motocycle, BrandsMotocycle
import csv

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


def create_brand(brand):
    list_brands = [brand.brand_name for brand in BrandsMotocycle.query.all()]
    if brand in list_brands:
        return BrandsMotocycle.query.filter_by(brand_name=brand).one().id
    else:
        db.session.add(BrandsMotocycle(brand))
        db.session.commit()
        return BrandsMotocycle.query.filter_by(brand_name=brand).one().id


def get(id):
    if isinstance(id, int):
        count_vehicles = Motocycle.query.filter_by(id=id).count()
        if count_vehicles:
            motocycle = Motocycle.query.filter_by(id=id).one()
            return motocycle
            #return motocycle.to_dict()
        return {'error':'There is no motocycle, wrong id.'}
    return {'error':'Wrong format "id"'}


def take_gears():
    gears = Motocycle.query.distinct(Motocycle.gear_type).all()
    for i in gears:
        print(i.gear_type)


def class_cycles():
    classes = Motocycle.query.distinct(Motocycle.cycle_class).all()
    for i in classes:
        print(i.cycle_class)


def engine_size(size=None):
    if size:
        moto = Motocycle.query.filter(Motocycle.engine > 999).all()
        for i in moto:
            print(i.model, i.engine)



if __name__ == '__main__':
    #x = BrandsMotocycle.query.all()
    #class_cycles()
    engine_size(9)
