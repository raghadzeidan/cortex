import flask
import click
from ..api import run_api_server
import requests

@click.group()
def cli():
    pass

@cli.command('get-users')
@click.option('-h', '--host', default='127.0.0.1', help="This should include what host to 'reflect' api from") 
@click.option('-p', '--port', default=5000, help="This should include what port to 'reflect' api from")
def get_users(host, port,mq):
	requests.get



cli()
