from flask_restplus import Api
from .cone import namespace as namespace_cone
from .hardware import namespace as namespace_hw
# from .port import namespace as namespace_port
# from .error import namespace as namespace_error
# from .param import namespace as namespace_empty_tube
from .configuration import namespace as namespce_config
from .csv_report import namespace as namespace_report
# from .available_ports import namespace as namespace_port_available

api = Api(
    title='Wall of APIs',
    version='1.0',
    description='A repo to host the APIs',
)

api.add_namespace(namespace_cone)
api.add_namespace(namespace_hw)
# api.add_namespace(namespace_port)
# api.add_namespace(namespace_error)
# api.add_namespace(namespace_empty_tube)
api.add_namespace(namespce_config)
api.add_namespace(namespace_report)
# api.add_namespace(namespace_port_available)
