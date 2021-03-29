from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api import config
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


class Motocycle(db.Model, SerializerMixin):
    def __init__(self, brand_name, model):
        self.brand_name = brand_name
        self.model = model
    __tablename__ = 'motocycles_info'
    id = db.Column(db.Integer, primary_key=True)
    #brand_name = db.relationship('BrandsMotocycle', db.ForeignKey('BrandsMotocycle.id'), lazy='joined')
    brand_name = db.Column(db.Integer, db.ForeignKey('brands.id'))
    model = db.Column(db.String(100))
    modifications = db.Column(db.String(300))
    year_birth = db.Column(db.String(150))
    engine = db.Column(db.SmallInteger)
    horse_power = db.Column(db.String(300))
    torque = db.Column(db.String(300))
    cylinders = db.Column(db.SmallInteger)
    type_engine = db.Column(db.String(200))
    gear_type = db.Column(db.String(50))
    cycle_class = db.Column(db.String(50))
    abs = db.Column(db.Boolean)


    def __repr__(self):
        return f'{self.brand_name} {self.model}'


    def print_properties(self):
        return f'{self.__dict__}'


class BrandsMotocycle(db.Model, SerializerMixin):
    def __init__(self, brand_name):
        self.brand_name = brand_name
    __tablename__ = 'brands'
    #brand_id = db.Column(db.Integer, backref='id', primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    motos = db.relationship(Motocycle, backref='brands', lazy='joined')
    brand_name = db.Column(db.String(100))
    def __repr__(self):
        return f'{self.brand_name} {self.id}'


def create_brand(brand):
    list_brands = [brand.brand_name for brand in BrandsMotocycle.query.all()]
    if brand in list_brands:
        return BrandsMotocycle.query.filter_by(brand_name=brand).first().id
    else:
        db.session.add(BrandsMotocycle(brand))
        db.session.commit()
        return BrandsMotocycle.query.filter_by(brand_name=brand).first().id


if __name__ == '__main__':
    db.create_all()

