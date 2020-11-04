from sqlalchemy import Column, Integer, String, Float
from config import db


class ErrorConfiguration(db.Model):
    __tablename__ = 'error'
    id = Column(Integer, primary_key=True)
    min_density = Column(Float)
    max_density = Column(Float)
    min_outer_diameter = Column(Float)
    max_outer_diameter = Column(Float)
    min_weight = Column(Float)
    max_weight = Column(Float)

    def __repr__(self):
        return super().__repr__()
