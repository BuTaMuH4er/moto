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

if __name__ == '__main__':
    a = Motocycle.query.filter_by(id=50).one()
    b = BrandsMotocycle.query.filter_by(id=a.brand_name).one()
    print(b.brand_name, a.model)