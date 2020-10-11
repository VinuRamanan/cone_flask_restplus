from flask_restplus import Resource, Namespace
from resources.ports import serial_ports

namespace = Namespace('COMPorts', description='Port related Operations')


@namespace.route('')
class Ports(Resource):
    @namespace.doc('Get all the active ports')
    def get(self):
        t = [{'name': port[:3], 'value':port[3:]} for port in serial_ports()]
        if len(t) == 0:
            return {'ports': [{'name': 'com'}]}
        return {'ports': t}
