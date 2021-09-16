from better_rest.routing.rest_route import RestRoute
from better_rest.routing.rest_router import RestRouter


class DummyRoute(RestRoute):
    name = 'test'
    path = '/test'

    async def get(self):
        return 'fromage'

    async def post(self):
        return 'fromage'

    async def put(self):
        return 'fromage'

    async def delete(self):
        return 'fromage'


class DummyRouter(RestRouter):
    name = 'test'
    path = '/test'
    sub_route_0 = DummyRoute
    sub_route_1 = DummyRoute.as_route()
