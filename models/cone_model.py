from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
import time
from config import db


class ConeRecord(db.Model):
    __tablename__ = 'cone_records'

    id = Column(Integer, primary_key=True)
    time_stamp = Column(Integer, default=int(
        time.time()), onupdate=int(time.time()))
    lot_number = Column(String)
    yarn_type = Column(String)
    customer_name = Column(String)
    lot_weight = Column(Float)
    yarn_count = Column(String)
    lot_height = Column(Float)
    sample_number = Column(Integer)
    density = Column(Float)
    spindle_number = Column(Float)
    error_type = Column(String)
    laser_raw_output = Column(Float)
    outer_radius = Column(Float)
    volume = Column(Float)
    weight_raw_output = Column(Float)
    mass = Column(Float)
    barcode_raw_input = Column(Float)

    def __repr__(self):
        return super().__repr__()
