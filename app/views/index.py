from sanic.response import file


async def index(_):
    return await file('app/templates/index.html')
