from flask import Flask, request
from flask_restplus import Namespace, Resource, fields, reqparse
import random
from resources.density import Density

DENSITY_OBJECT = Density()


namespace = Namespace(
    'Data', description='Generating randomized values for parameters that are either hardware or calculated')

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
    'barcode_raw_input': fields.Float(
        required=True,
        description='Barcode Raw Input'
    ),
    'weight': fields.Float(
        required=True,
        description='Barcode Raw Input'
    ),
})


@namespace.route('/generator')
class RandomDataGenerator(Resource):
    @namespace.marshal_with(generate_output_model)
    def get(self):
        t = random.randint(0, 1)
        data = {'density': random.random()*random.randint(1, 1000),
                'laser_raw_output': random.random()*random.randint(1, 1000),
                'outer_diameter': random.random()*random.randint(1, 1000),
                'volume': random.random()*random.randint(1, 1000),
                'weight_raw_output': random.random()*random.randint(1, 1000),
                'mass': random.random()*random.randint(1, 1000),
                'weight': random.random()*random.randint(1, 1000),
                'error_type': 'Error' if t else 'No Error',
                'barcode_raw_input': random.random()*random.randint(1, 1000)}
        return data


@namespace.route('/calculator')
class DataCalculator(Resource):
    @namespace.marshal_with(generate_output_model)
    def get(self):
        t = random.randint(0, 1)

        params = DENSITY_OBJECT.get_params()
        data = {'error_type': 'Error' if t else 'No Error'}
        params.update(data)
        return params
