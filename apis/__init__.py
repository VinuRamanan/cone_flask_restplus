from flask_restplus import Api
from .cone import namespace as namespace_cone
from .generator import namespace as namespace_generate

api = Api(
    title='Wall of APIs',
    version='1.0',
    description='A repo to host the APIs',
)

api.add_namespace(namespace_cone)
api.add_namespace(namespace_generate)
