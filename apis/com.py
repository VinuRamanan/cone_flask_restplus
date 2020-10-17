from flask_restplus import Resource, Namespace, fields
from resources.ports import serial_ports
from models.port_model import Port
from config import db
from flask import request
import json

namespace = Namespace('COMPorts', description='Port related Operations')

input_model = namespace.model('PortModel', {
    'weight_port': fields.String(required=True),
    'laser_port': fields.String(required=True)
})


@namespace.route('/AvailablePorts')
class AvailablePorts(Resource):
    @namespace.doc('Get all the active ports')
    def get(self):
        return {'ports': [{'name': port[:3], 'value':port[3:]} for port in serial_ports()]}


@namespace.route('/Ports')
class Ports(Resource):
    @namespace.doc('Get the recently set Laser and Weight Port')
    def get(self):
        data = Port.query.filter_by(id=1).first()
        return {'weight_port': data.weight_port, 'laser_port': data.laser_port}

    @namespace.doc('Update the Laser and Weight Port')
    @namespace.expect(input_model, validate=True)
    def post(self):
        data = json.loads(request.data)
        existing = Port.query.filter_by(id=1).first()
        existing.weight_port = data['weight_port']
        existing.laser_port = data['laser_port']
        db.session.commit()
        return {'status': 1,
                'message': 'Updated the Laser Port and Weight Port'
                }
