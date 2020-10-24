from flask import Flask, request
from flask_restplus import Namespace, Resource, fields, reqparse
from config import db
from models.cone_model import ConeRecord
from sqlalchemy import desc
import inspect
from config import db
from flask_csv import send_csv
import inspect
from models.cone_model import ConeRecord

namespace = Namespace('report', description='Cone Records CSV Report')


@namespace.route('/customer_name=<string:customer_name>&lot_number=<string:lot_number>&spindle_number=<string:spindle_number>&start_row=<int:start_row>&limit=<int:limit>')
class ConeData(Resource):

    @namespace.doc(responses={204: 'No content'})
    def get(self, customer_name, spindle_number, lot_number, start_row, limit):
        records = ConeRecord.query.filter(
            ConeRecord.customer_name.like(customer_name)
        ).filter(
            ConeRecord.lot_number.like(lot_number)
        ).filter(
            ConeRecord.spindle_number.like(spindle_number)
        ).order_by(
            desc(ConeRecord.id)
        ).slice(start_row, start_row+limit)
        data = []
        fields = ['date', 'lot_number', 'yarn_type', 'customer_name', 'lot_weight', 'yarn_count', 'start_lot_height', 'end_lot_height', 'sample_number',
                  'density', 'spindle_number', 'error_type', 'laser_raw_output', 'outer_diameter', 'volume', 'weight_raw_output', 'mass', 'weight']
        for record in records:
            datum = {attr: getattr(record, attr) for attr in fields}
            data.append(datum)
        return send_csv(data, filename='report.csv', fields=fields)
