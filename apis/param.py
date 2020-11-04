from flask_restplus import Resource, Namespace, fields
from resources.ports import serial_ports
from models.param_model import ParamModel
from config import db
from flask import request
import json

namespace = Namespace('param',
                      description='Param related Operations')

input_model = namespace.model('ParamModel', {
    'empty_tube_diameter': fields.Float(required=True),
    'calibration': fields.Float(required=True)
})


@namespace.route('')
class Param(Resource):
    @namespace.doc('Get the recently set Empty Tube Diameter')
    def get(self):
        data = ParamModel.query.filter_by(id=1).first()
        return {
            'empty_tube_diameter': data.empty_tube_diameter,
            'calibration': data.calibration
        }

    @namespace.doc('Update the Empty Tube Diameter')
    @namespace.expect(input_model, validate=True)
    def post(self):
        data = json.loads(request.data)
        existing = ParamModel.query.filter_by(id=1).first()
        for key, value in data.items():
            setattr(existing, key, value)
        db.session.commit()
        return {'status': 1,
                'message': 'Updated the Empty Tube Diameter'
                }
