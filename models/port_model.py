from sqlalchemy import Column, Integer, String
from config import db


class Port(db.Model):
    __tablename__ = 'ports'

    id = Column(Integer, primary_key=True)
    laser_port = Column(String)
    weight_port = Column(String)

    def __repr__(self):
        return super().__repr__()
