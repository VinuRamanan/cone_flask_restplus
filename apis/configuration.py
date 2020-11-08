from flask_restplus import Resource, Namespace, fields
from resources.ports import serial_ports
from models.param_model import ParamModel
from models.error_model import ErrorConfiguration as ErrorConfigurationModel
from models.port_model import Port
from config import db
from flask import request
import json


namespace = Namespace('configuration', description='Configuration Vars')


error_input_model = namespace.model('ErrorModel', {
    'min_weight': fields.Float(required=True),
    'max_weight': fields.Float(required=True),
    'min_density': fields.Float(required=True),
    'max_density': fields.Float(required=True),
    'min_outer_diameter': fields.Float(required=True),
    'max_outer_diameter': fields.Float(required=True)
})

param_input_model = namespace.model('ParamModel', {
    'empty_tube_diameter': fields.Float(required=True),
    'calibration': fields.Float(required=True)
})

port_input_model = namespace.model('PortModel', {
    'weight_port': fields.String(required=True),
    'laser_port': fields.String(required=True)
})


@namespace.route('/error')
class Errors(Resource):
    @namespace.doc('Get the recently set Error Configuration')
    def get(self):
        data = ErrorConfigurationModel.query.filter_by(id=1).first()
        return {
            'min_weight': data.min_weight,
            'max_weight': data.max_weight,
            'min_density': data.min_density,
            'max_density': data.max_density,
            'min_outer_diameter': data.min_outer_diameter,
            'max_outer_diameter': data.max_outer_diameter
        }

    @namespace.doc('Update the Error Configuration')
    @namespace.expect(error_input_model, validate=True)
    def post(self):
        data = json.loads(request.data)
        existing = ErrorConfigurationModel.query.filter_by(id=1).first()
        for key, value in data.items():
            setattr(existing, key, value)
        db.session.commit()
        return {'status': 1,
                'message': 'Updated the Error Configuration'
                }


@namespace.route('/param')
class Param(Resource):
    @namespace.doc('Get the recently set Empty Tube Diameter')
    def get(self):
        data = ParamModel.query.filter_by(id=1).first()
        return {
            'empty_tube_diameter': data.empty_tube_diameter,
            'calibration': data.calibration
        }

    @namespace.doc('Update the Empty Tube Diameter')
    @namespace.expect(param_input_model, validate=True)
    def post(self):
        data = json.loads(request.data)
        existing = ParamModel.query.filter_by(id=1).first()
        for key, value in data.items():
            setattr(existing, key, value)
        db.session.commit()
        return {'status': 1,
                'message': 'Updated the Empty Tube Diameter'
                }


@namespace.route('/port')
class Ports(Resource):
    @namespace.doc('Get the recently set Laser and Weight Port')
    def get(self):
        data = Port.query.filter_by(id=1).first()
        return {'weight_port': data.weight_port, 'laser_port': data.laser_port}

    @namespace.doc('Update the Laser and Weight Port')
    @namespace.expect(port_input_model, validate=True)
    def post(self):
        data = json.loads(request.data)
        existing = Port.query.filter_by(id=1).first()
        for key, value in data.items():
            setattr(existing, key, value)
        db.session.commit()
        return {'status': 1,
                'message': 'Updated the Laser Port and Weight Port'
                }


@namespace.route('/available_ports')
class AvailablePorts(Resource):
    @namespace.doc('Get all the active ports')
    def get(self):
        return {'ports': [{'name': port, 'value': port} for port in serial_ports()]}
