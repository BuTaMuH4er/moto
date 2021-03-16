from flask_sqlalchemy import SQLAlchemy
from db_settings import Base, engine_db


db = SQLAlchemy()


class Motocycle(db.Model):
    def __init__(self, brand_name, model):
        self.brand_name = brand_name
        self.model = model
    __tablename__ = 'motocycles_info'
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String)
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


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine_db)
