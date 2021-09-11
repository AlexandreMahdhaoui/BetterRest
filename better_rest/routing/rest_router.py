import typing

from starlette.routing import Mount, Route

from better_rest.routing.rest_route import RestRoute


class RestRouter:
    """
    Usage:
        Create a class Fromage inheriting from RestRouter with sub- Mount/Route as Fromage's attributes.
        The class Fromage can return:
            -> a list of sub- starlette.routing.Mount/Route objects.

            -> a starlette.routing.Mount of sub- starlette.routing.Mount or Route objects.
    attr:
        - name: str => Sets name of the starlette.routing.Mount returned by cls.as_mount(). Default: cls.__name__.lower()
        - path: str => Sets path of the starlette.routing.Mount returned by cls.as_mount(). Default: cls.__name__.lower()
    methods:
        - as_list() => Returns a list of starlette.routing.Mount or Route objects
        - as_mount() => Returns a Mount of name cls.__name__ or cls.name
    Example:
        >> class Fromage(RestRouter):
            camembert_sub_route: CamembertRoute
            cheddar_sub_mount: CheddarMount
        # CamembertRoute is a class inheriting from RestRoute
    """
    name: str
    path: str
    prohibited_keys = ['name', 'path', 'prohibited_keys']

    @classmethod
    def as_list(cls, ):
        return [cls._sanitize(v) for k, v in cls.__dict__.items() if not k.startswith('_') and k not in cls.prohibited_keys]

    @classmethod
    def as_mount(cls):
        name = cls.name if hasattr(cls, 'name') else cls.__name__.lower()
        path = cls.path if hasattr(cls, 'path') else "/" + name
        routes = cls.as_list()
        return Mount(name=name, path=path, routes=routes)

    @classmethod
    def _sanitize(cls, v: typing.Union[Mount, Route, RestRoute, 'RestRouter']):
        if isinstance(v, Mount) or isinstance(v, Route):
            return v
        if cls.__base__ in v.__bases__:
            return v.as_mount()
        if RestRoute in v.__bases__:
            return v.as_route()
