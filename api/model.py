from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from db_settings import Base, engine_db
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
    brand_name = db.relationship('BrandsMotocycle', backref='brand', lazy='dynamic')
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
    brand_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('brand.id'))
    brand_name = db.Column(db.String(100))
    def __repr__(self):
        return f'{self.brand_name} {self.brand_id}'


if __name__ == '__main__':
    db.create_all()
