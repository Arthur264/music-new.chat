from signal import signal, SIGINT

import asyncio
import click
import uvloop
from sanic.websocket import WebSocketProtocol

from app.main import create_app


@click.group()
@click.option('--debug/--no-debug', default=True)
@click.pass_context
def cli(ctx, debug):
    ctx.obj = {}
    ctx.obj['DEBUG'] = debug
    click.echo(f'Debug mode is {debug}')


@cli.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default='8080', type=int)
@click.option('--access_log', default=False, type=bool)
@click.pass_context
def runserver(ctx, host, port, access_log):
    app = create_app()
    app.run(
        debug=ctx.obj['DEBUG'],
        workers=1,
        host=host,
        port=port,
        backlog=1,
        access_log=access_log,
        protocol=WebSocketProtocol,
        auto_reload=ctx.obj['DEBUG'],
    )
    asyncio.set_event_loop(uvloop.new_event_loop())
    server = app.create_server(host="0.0.0.0", port=8000)
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(server)
    signal(SIGINT, lambda s, f: loop.stop())
    try:
        loop.run_forever()
    except:
        loop.stop()


if __name__ == '__main__':
    cli()
