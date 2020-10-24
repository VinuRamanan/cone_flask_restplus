from flask_restplus import Api
from .cone import namespace as namespace_cone
from .generator import namespace as namespace_generate
from .density import namespace as namespace_density
from .com import namespace as namespace_com
from .configuration import namespace as namespace_conf
from .empty_tube import namespace as namespace_empty_tube
from .csv_report import namespace as namespace_report

api = Api(
    title='Wall of APIs',
    version='1.0',
    description='A repo to host the APIs',
)

api.add_namespace(namespace_cone)
api.add_namespace(namespace_generate)
api.add_namespace(namespace_density)
api.add_namespace(namespace_com)
api.add_namespace(namespace_conf)
api.add_namespace(namespace_empty_tube)
api.add_namespace(namespace_report)
