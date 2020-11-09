from sqlalchemy.ext.declarative import declarative_base
import datetime as dt
from sqlalchemy import Column, Integer, String, Float, Date
import time
from config import db


class ConeRecord(db.Model):
    __tablename__ = 'cone_records'

    id = Column(Integer, primary_key=True)
    time_stamp = Column(Integer, default=int(
        time.time()), onupdate=int(time.time()))
    date = Column(Date, default=dt.datetime.now, onupdate=dt.datetime.now)
    lot_number = Column(String)
    yarn_type = Column(String)
    customer_name = Column(String)
    lot_weight = Column(Float)
    yarn_count = Column(String)
    start_lot_height = Column(Float)
    end_lot_height = Column(Float)
    sample_number = Column(Integer)
    density = Column(Float)
    spindle_number = Column(String)
    error_type = Column(String)
    laser_raw_output = Column(Float)
    outer_diameter = Column(Float)
    volume = Column(Float)
    weight_raw_output = Column(Float)
    weight = Column(Float)

    def __repr__(self):
        return super().__repr__()


db.create_all()
db.session.commit()
