from cassandra.cqlengine.query import LWTException
from sanic.views import HTTPMethodView

from app.http import error_response, json_response
from app.utils.request import check_uuid


class ModelBaseView(HTTPMethodView):
    model = None

    @staticmethod
    async def _make_request(data, many=False):
        if not data:
            return await json_response({})

        if many:
            return await json_response([item.to_dict() for item in data])

        if isinstance(data, list):
            return await json_response(data[0].to_dict())

        return await json_response(data.to_dict())

    @check_uuid
    async def get(self, request):
        param_id = request.raw_args.get('id')
        if not param_id:
            instances = self.model.objects().all()
            return await self._make_request(instances, many=True)

        instance = self.model.objects(id=param_id)
        if not instance:
            model_name = self.model.__name__.replace('Model', '')
            return await error_response(msg=f'{model_name} not found',
                                        status=404)

        return await self._make_request(instance)

    async def post(self, request):
        try:
            data = self.prepare_data(request)
            instance = self.model.if_not_exists().create(**data)
            return await self._make_request(instance)
        except LWTException:
            return await error_response(msg=f'Instance already exist.',
                                        status=400)

    @staticmethod
    def prepare_data(request):
        return request.json

    @check_uuid
    async def delete(self, request):
        param_id = request.raw_args.get('id')
        instance = self.model.objects(id=param_id)
        if not instance:
            model_name = self.model.__name__.replace('Model', '')
            return await error_response(msg=f'{model_name} not found',
                                        status=404)

        return await self._make_request(instance)
