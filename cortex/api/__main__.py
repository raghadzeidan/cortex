import click
from .api import run_api_server

@click.group()
def cli():
    pass


@cli.command('run-server')
@click.argument('host')
@click.argument('port')
@click.argument('db_url')
def microservice_run_saver(host, port, db_url):
	run_api_server(host,port, db_url)
	
cli()
