from flask_restplus import Resource, Namespace
from resources.ports import serial_ports

namespace = Namespace('COMPorts', description='Port related Operations')


@namespace.route('')
class Ports(Resource):
    @namespace.doc('Get all the active ports')
    def get(self):
        return {'ports': serial_ports()}
