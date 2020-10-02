from flask_restplus import Namespace, Resource
from resources.density import Density

namespace = Namespace(
    'Density', description='Returns the Density at the moment')

DENSITY_OBJECT = Density()


@namespace.route('density')
class DensityResource(Resource):
    def get(self):
        return DENSITY_OBJECT.get_density()
