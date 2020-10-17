from flask_restplus import Resource, Namespace, fields
from resources.ports import serial_ports
from models.configuration_model import Configuration as ConfigurationModel
from config import db
from flask import request
import json

namespace = Namespace('Configuration', description='Port related Operations')

input_model = namespace.model('PortModel', {
    'min_weight': fields.Float(required=True),
    'max_weight': fields.Float(required=True),
    'min_density': fields.Float(required=True),
    'max_density': fields.Float(required=True),
    'min_outer_diameter': fields.Float(required=True),
    'max_outer_diameter': fields.Float(required=True)
})


@namespace.route('')
class Configuration(Resource):
    @namespace.doc('Get the recently set Configuration')
    def get(self):
        data = ConfigurationModel.query.filter_by(id=1).first()
        return {
            'min_weight': data.min_weight,
            'max_weight': data.max_weight,
            'min_density': data.min_density,
            'max_density': data.max_density,
            'min_outer_diameter': data.min_outer_diameter,
            'max_outer_diameter': data.max_outer_diameter
        }

    @namespace.doc('Update the Configuration')
    @namespace.expect(input_model, validate=True)
    def post(self):
        data = json.loads(request.data)
        existing = ConfigurationModel.query.filter_by(id=1).first()
        for key, value in data.items():
            setattr(existing, key, value)
        db.session.commit()
        return {'status': 1,
                'message': 'Updated the Configuration'
                }
