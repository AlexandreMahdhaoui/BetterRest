import json
from starlette.responses import JSONResponse, Response

from better_rest.routing.rest_route import RestRoute
from better_rest.routing.rest_router import RestRouter
from better_rest.utils import init_service_dict


class BetterRest(RestRouter):
    """
    Class used to create a REST API from default_config
    """
    _name = 'rest'
    _namespace = dict
    _meta_conf = dict
    path = '/api'
    prohibited_keys = ['name', 'path', 'prohibited_keys', 'routes']

    def __init__(
            self,
            name,
            namespace
    ):
        self._name = name
        self._namespace = namespace
        self._meta_conf = namespace[name]['meta_conf']
        self._init_graph_api()
        self._init_service_api()
        self._init_from_config()

    @property
    def routes(self):
        return self.as_mount()

    def _init_graph_api(self):
        graph = self._namespace[self._meta_conf['graph']['provider']]['instance']

        class GraphApi(RestRoute):
            name = 'graph'
            path = '/graph'

            async def post(self, request):
                try:
                    data = json.loads(request.body())['data']
                    return JSONResponse({
                        'status': 'success',
                        'data': graph(data)
                    })
                except:
                    return Response(status_code=500)

        self.graph_api = GraphApi.as_route()

    def _init_service_api(self):
        """
        exposes /services/{service_name}/{path_param}
        :return:
        """
        services = dict()
        services_ = self._namespace[self._meta_conf['services']['provider']]['instance']
        for service in services_:
            name = service['name']
            service_ = init_service_dict(service)
            services[name] = type(service, (RestRoute,), {
                'name': name,
                'path': name+'/{path_param}',
                **service_
            })
        self.service_api = type('ServiceApi', (RestRouter,), {
            'name': 'services',
            'path': '/services',
            **services
        })

    def _init_from_config(self):
        pass
