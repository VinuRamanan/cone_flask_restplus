from sqlalchemy import Column, Integer, String, Float
from config import db


class Configuration(db.Model):
    __tablename__ = 'configuration'
    #density, outer_radius, weight
    id = Column(Integer, primary_key=True)
    min_density = Column(Float)
    max_density = Column(Float)
    min_outer_radius = Column(Float)
    max_outer_radius = Column(Float)
    min_weight = Column(Float)
    max_weight = Column(Float)

    def __repr__(self):
        return super().__repr__()
