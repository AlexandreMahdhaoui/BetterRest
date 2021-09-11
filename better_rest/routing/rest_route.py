from starlette.endpoints import HTTPEndpoint
from starlette.routing import Route


class RestRoute:
    """
    Usage:
        Programmatically creates a starlette.endpoints.Endpoint and starlette.routing.Route
        Super class of ROUTE object returning a starlette.routing.Route
    attr:
        name: str => default: cls.__name__.lower()
        path: str => default: cls.__name__.lower()
    methods:
        as_route()
    Example:
        >> class Camembert(RestRoute):
            async def get(self, request):
                return PlainTextResponse("HelloWorld!")
        # To programmatically create an object inheriting from RestRoute:
        >> type(
            'Camembert',
            (RestRoute,)
            {
                'get': async def get(self, request):
                    return PlainTextResponse("HelloWorld!"
            }
        )
    """
    name: str
    path: str
    methods = ['get', 'post', 'put', 'delete']

    @classmethod
    def as_route(cls):
        name = cls.name if hasattr(cls, 'name') else cls.__name__.lower()
        path = cls.path if hasattr(cls, 'path') else "/" + name
        return Route(
            name=name,
            path=path,
            endpoint=cls._get_endpoint()
        )

    @classmethod
    def _get_endpoint(cls):
        name = cls.__name__
        bases = (HTTPEndpoint,)
        dict_ = cls._get_methods()
        return type(name, bases, dict_)

    @classmethod
    def _get_methods(cls):
        return {k: v for k, v in cls.__dict__.items() if k in cls.methods}
