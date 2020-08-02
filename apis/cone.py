from flask import Flask
from flask_restplus import Namespace, Resource, fields

namespace = Namespace('cone', description='Cone Related Operations')

output_model = namespace.model('Greeting', {'message': fields.String(
    required=True, description='Just a greeting')})


@namespace.route('')
class Cone(Resource):
    @namespace.marshal_list_with(output_model)
    def get(self):
        return {'message': 'This is the cone API'}
