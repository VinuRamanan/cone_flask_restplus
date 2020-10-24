from flask import Flask, request
from flask_restplus import Namespace, Resource, fields, reqparse
from config import db
from models.cone_model import ConeRecord
from sqlalchemy import desc

import json


namespace = Namespace('cone', description='Cone Related Operations')

output_model = namespace.model('Greeting', {'message': fields.String(
    required=True, description='Just a greeting')})

insert_input_model = namespace.model('Cone Record', {
    'lot_number': fields.Integer(
        required=True,
        description='Lot Number'
    ),
    'yarn_type': fields.String(
        required=True,
        description='Yarn Type'
    ),
    'customer_name': fields.String(
        required=True,
        description='Customer Name'
    ),
    'lot_weight': fields.Float(
        required=True,
        description='Lot Weight'
    ),
    'yarn_count': fields.String(
        required=True,
        description='Yarn Count'
    ),
    'start_lot_height': fields.Float(
        required=True,
        description='Height'
    ),
    'end_lot_height': fields.Float(
        required=True,
        description='Height'
    ),
    'weight': fields.Float(
        required=True,
        description='Height'
    ),
    'sample_number': fields.Integer(
        required=True,
        description='Sample Number'
    ),
    'density': fields.Float(
        required=True,
        description='Density'
    ),
    'spindle_number': fields.String(
        required=True,
        description='Spindle Number'
    ),
    'error_type': fields.String(
        required=True,
        description='Error Type'
    ),
    'laser_raw_output': fields.Float(
        required=True,
        description='Laser Raw Output'
    ),
    'outer_diameter': fields.Float(
        required=True,
        description='Outer Radius'
    ),
    'volume': fields.Float(
        required=True,
        description='Volume'
    ),
    'weight_raw_output': fields.Float(
        required=True,
        description='Weight Raw Output'
    ),
    'mass': fields.Float(
        required=True,
        description='Mass'
    ),
})

insert_output_model = namespace.model('Insertion Response',
                                      {
                                          'response': fields.String(
                                              required=True,
                                              description='Response for insertion of a cone'
                                          )
                                      })


@namespace.route('')
class Cone(Resource):

    @namespace.expect(insert_input_model, validate=True)
    @namespace.marshal_with(insert_output_model)
    def post(self):
        data = json.loads(request.data)
        cone = ConeRecord(**data)
        try:
            db.session.add(cone)
            response = {'response': 'Inserted successfully'}
        except BaseException as e:
            print(e)
            response = {'response': 'Insertion Failed'}
        finally:
            db.session.commit()
            return response


@namespace.route('/customer_name=<string:customer_name>&lot_number=<string:lot_number>&spindle_number=<string:spindle_number>&start_row=<int:start_row>&limit=<int:limit>')
class ConeData(Resource):

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
        data = [[record.sample_number, record.spindle_number, record.customer_name, record.lot_number, record.weight,
                 record.outer_diameter, record.density, record.error_type] for record in records]
        return {'count': len(data),
                'data': data}
        # end_row = start_row + min(len(records)-start_row, limit)
        # return records[start_row:end_row]
