from .server import run_server
import click

@click.group()
def cli():
    pass

@cli.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', help="this should specify the host address in which to run the server on") 
@click.option('-p', '--port', default=8000, help="this should specify the port number on which to run the server on")
@click.argument('mq')
def cli_run_server(host, port,mq ):
    print(mq)
    run_server(host, port,mq_url=mq)



cli()
