from flask import Flask, request
from flask_restplus import Namespace, Resource, fields, reqparse
from config import db
from models.cone_model import ConeRecord

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
    'lot_height': fields.Float(
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
    'spindle_number': fields.Float(
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
    'outer_radius': fields.Float(
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
    'barcode_raw_input': fields.Float(
        required=True,
        description='Barcode Raw Input'
    ),
})

insert_output_model = namespace.model('Insertion Response',
                                      {
                                          'response': fields.String(
                                              required=True,
                                              description='Response for insertion of a cone'
                                          )
                                      })


@ namespace.route('')
class Cone(Resource):
    @ namespace.marshal_list_with(output_model)
    def get(self):
        return {'message': 'This is the cone API'}

    @ namespace.expect(insert_input_model, validate=True)
    @ namespace.marshal_with(insert_output_model)
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
