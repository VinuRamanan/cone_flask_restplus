from flask_restplus import Resource, Namespace, fields
from resources.ports import serial_ports
from models.empty_tube_model import EmptyTubeModel
from config import db
from flask import request
import json

namespace = Namespace('Param',
                      description='Param related Operations')

input_model = namespace.model('Param', {
    'empty_tube_diameter': fields.Float(required=True),
})


@namespace.route('')
class EmptyTubeDiameter(Resource):
    @namespace.doc('Get the recently set Empty Tube Diameter')
    def get(self):
        data = EmptyTubeModel.query.filter_by(id=1).first()
        return {
            'empty_tube_diameter': data.empty_tube_diameter
        }

    @namespace.doc('Update the Empty Tube Diameter')
    @namespace.expect(input_model, validate=True)
    def post(self):
        data = json.loads(request.data)
        existing = EmptyTubeModel.query.filter_by(id=1).first()
        for key, value in data.items():
            setattr(existing, key, value)
        db.session.commit()
        return {'status': 1,
                'message': 'Updated the Empty Tube Diameter'
                }
