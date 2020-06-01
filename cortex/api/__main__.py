import click
from .api import run_api_server

@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', help="this should specify the host address in which to run the gui server on") 
@click.option('-p', '--port', default=5000, help="this should specify the port number on which to run the gui server on")
@click.option('-d','--database', default='mongodb://127.0.0.1:27017')
def microservice_run_saver(host, port, database):
	run_api_server(host,port, database)
	
cli()
