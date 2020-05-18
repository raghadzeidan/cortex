import click
from .saver_main import run_saver_as_microservice

@click.group()
def cli():
    pass


@cli.command('run-saver')
@click.argument('db_url')# help='this should contain a url of the format db://host:port for the saver to save data into')
@click.argument('mq_url')# help='this should contain a url of the format mq://host:port for the saver to consume data from')
def microservice_run_saver(db_url, mq_url):
	run_saver_as_microservice(db_url, mq_url)
	
cli()
