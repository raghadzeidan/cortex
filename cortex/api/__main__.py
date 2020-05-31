import click
from .api import run_api_server

@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', help="this should specify the host address in which to run the gui server on") 
@click.option('-p', '--port', default=5000, help="this should specify the port number on which to run the gui server on")
@click.optin('-d','--database', default="")
def microservice_run_saver(host, port, db_url):
	run_api_server(host,port, db_url)
	
cli()
