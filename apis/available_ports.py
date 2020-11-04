from flask_restplus import Resource, Namespace
from resources.ports import serial_ports

namespace = Namespace('available_ports', description='Port related Operations')


@namespace.route('')
class AvailablePorts(Resource):
    @namespace.doc('Get all the active ports')
    def get(self):
        return {'ports': [{'name': port[:3], 'value':port[3:]} for port in serial_ports()]}
