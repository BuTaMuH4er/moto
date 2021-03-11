from sqlalchemy import Column, Integer, String, Boolean, SmallInteger
from db import Base, engine_db


class Motocycle(Base):
    def __init__(self, brand_name, model):
        self.brand_name = brand_name
        self.model = model
    __tablename__ = 'motocycles_info'
    id = Column(Integer, primary_key=True)
    brand_name = Column(String)
    model = Column(String(100))
    modifications = Column(String(300))
    year_birth = Column(String(50))
    engine = Column(SmallInteger)
    horse_power = Column(String(300))
    torque = Column(String(300))
    cylinders = Column(SmallInteger)
    type_engine = Column(String(200))
    gear_type = Column(String(50))
    cycle_class = Column(String(50))
    abs = Column(Boolean)

    def __repr__(self):
        return f'{self.brand_name} {self.model}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine_db)
