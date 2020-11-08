from flask import Flask, request
from flask_restplus import Namespace, Resource, fields, reqparse
from resources.density import weight_machine_config, laser_sensor_config
import random
from resources.density import *
from models.param_model import ParamModel
from resources import weight_object, laser_object
import json


data = ParamModel.query.filter_by(id=1).first()
DESIGN_ERROR = data.calibration
TUBE_RAD = data.empty_tube_diameter
FIXED_LENGTH = 200 + DESIGN_ERROR
PI = 3.14
TO_DECIMETER = 1/100
To_MILLIMETER = 100

namespace = Namespace(
    'hardware', description='Generating randomized values for parameters that are either hardware or calculated')


generate_input_model = namespace.model('InputModelForCalculator', {
    'empty_tube_diameter': fields.Float(required=True, description='Empty Tube Diameter'),
    'start_lot_height': fields.Float(required=True, description='Start Lot Height'),
    'end_lot_height': fields.Float(required=True, description='End Lot Height'),
    'calibration': fields.Float(required=True, description='Calibration value for error')
})

generate_output_model = namespace.model('Randomized calculated or hardware data', {
    'density': fields.Float(
        required=True,
        description='Density'
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
    'weight': fields.Float(
        required=True,
        description='Barcode Raw Input'
    ),
})


@namespace.route('/generate')
class RandomDataGenerator(Resource):
    # weight_object = weight_object
    # laser_object = laser_object

    @namespace.marshal_with(generate_output_model)
    def get(self):
        t = random.randint(0, 1)
        data = {'density': random.random()*random.randint(1, 1000),
                'laser_raw_output': random.random()*random.randint(1, 1000),
                'outer_diameter': random.random()*random.randint(1, 1000),
                'volume': random.random()*random.randint(1, 1000),
                'weight_raw_output': random.random()*random.randint(1, 1000),
                'mass': random.random()*random.randint(1, 1000),
                'weight': random.random()*random.randint(1, 1000)}
        return data


@namespace.route('/initialize/laser_port=<string:laser_port>&weight_port=<string:weight_port>')
class Initializer(Resource):
    # weight_object = weight_object
    # laser_object = laser_object

    def get(self, laser_port, weight_port):
        global weight_object, laser_object
        if not weight_object:
            weight_object = weight_machine_config(weight_port)
        if not laser_object:
            laser_object = laser_sensor_config(laser_port)
        if not weight_object and laser_object:
            msg = 'Weight Panjayath'
            status = 1
        elif weight_object and not laser_object:
            msg = 'Laser Panjayath'
            status = 2
        elif not weight_object and not laser_object:
            msg = 'Elaamae Panjayath'
            status = 3
        else:
            msg = 'Successful Initialization'
            status = 0
        code = 200 if not status else 500
        return {'status': status, 'message': msg}, code


@namespace.route('/calculator')
class Calculator(Resource):
    weight_object = weight_object
    laser_object = laser_object

    @namespace.expect(generate_input_model, validate=True)
    def post(self):
        global weight_object, laser_object
        data = json.loads(request.data)
        output = calculate(
            data['start_lot_height'], data['end_lot_height'], weight_object, laser_object, data['calibration'], data['empty_tube_diameter'])
        if output:
            return output, 200
        return None, 500
