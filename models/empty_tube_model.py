from sqlalchemy import Column, Float, Integer
from config import db


class EmptyTubeModel(db.Model):
    __tablename__ = 'empty_tube_diameter'

    id = Column(Integer, primary_key=True)
    empty_tube_diameter = Column(Float)

    def __repr__(self):
        return super().__repr__()
