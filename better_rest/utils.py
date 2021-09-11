import json
from functools import wraps

from starlette.requests import Request
from starlette.responses import JSONResponse, Response


def init_service_dict(service):
    service_ = dict()
    if service.get('create'):
        service_['post'] = endpoint_wrapper(service['create'])
    if service.get('read'):
        service_['get'] = endpoint_wrapper(service['read'])
    if service.get('update'):
        service_['put'] = endpoint_wrapper(service['update'])
    if service.get('delete'):
        service_['delete'] = endpoint_wrapper(service['delete'])
    return service_


async def endpoint_wrapper(func):
    @wraps(func)
    def wrapper(request: Request):
        try:
            body = await request.json()
            data = json.loads(body).get('data')
            path_param = request.path_params.get('path_param')
            if path_param and data:
                return JSONResponse({
                    'status': 'success',
                    'data': func(path_param, data)
                })
            if data:
                return JSONResponse({
                    'status': 'success',
                    'data': func(data)
                })
            if path_param:
                return JSONResponse({
                    'status': 'success',
                    'data': func(path_param)
                })
        except:
            return Response(status_code=500)

    return wrapper
