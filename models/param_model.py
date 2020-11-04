from sqlalchemy import Column, Float, Integer
from config import db


class ParamModel(db.Model):
    __tablename__ = 'param'

    id = Column(Integer, primary_key=True)
    empty_tube_diameter = Column(Float)
    calibration = Column(Float)

    def __repr__(self):
        return super().__repr__()
