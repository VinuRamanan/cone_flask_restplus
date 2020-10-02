from flask import Flask, request
from flask_restplus import Namespace, Resource, fields, reqparse
import random
from resources.density import Density

DENSITY_OBJECT = Density()


namespace = Namespace(
    'generator', description='Generating randomized values for parameters that are either hardware or calculated')

generate_output_model = namespace.model('Randomized calculated or hardware data', {
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


@namespace.route('')
class RandomDataGenerator(Resource):
    @namespace.marshal_with(generate_output_model)
    def get(self):
        t = random.randint(0, 1)

        params = DENSITY_OBJECT.get_params()
        data = {'spindle_number': 0.0,
                'error_type': 'Error' if t else 'No Error',
                'barcode_raw_input': 0.0}
        params.update(data)
        return params
