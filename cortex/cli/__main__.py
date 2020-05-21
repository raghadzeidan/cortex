import flask
import click
from ..api import run_api_server
import requests
import json

@click.group()
def cli():
	pass

@cli.command('get-users')
@click.option('-h', '--host', default='127.0.0.1', help="This should include what host to 'reflect' api from") 
@click.option('-p', '--port', default=5000, help="This should include what port to 'reflect' api from")
def get_users(host,port):
	'''Returns list of users''' 
	api_server_url = f'http://{host}:{port}/users'
	response = requests.get(api_server_url)
	print(response.json())
	
@cli.command('get-user')
@click.option('-h', '--host', default='127.0.0.1', help="This should include what host to 'reflect' api from") 
@click.option('-p', '--port', default=5000, help="This should include what port to 'reflect' api from")
@click.argument('user_id')
def get_user(host,port,user_id):
	'''Returns the specified user's details: ID, name, birthday and gender. '''
	api_server_url = f'http://{host}:{port}/users/{user_id}'
	response = requests.get(api_server_url)
	print(response.json())

@cli.command('get-snapshots')
@click.option('-h', '--host', default='127.0.0.1', help="This should include what host to 'reflect' api from") 
@click.option('-p', '--port', default=5000, help="This should include what port to 'reflect' api from")
@click.argument('user_id')
def get_snapshots(host,port,user_id):
	'''Returns the list of the specified user's snapshot IDs and datetimes only. '''
	api_server_url = f'http://{host}:{port}/users/{user_id}/snapshots'
	response = requests.get(api_server_url)
	print(response.json())

@cli.command('get-snapshot')
@click.option('-h', '--host', default='127.0.0.1', help="This should include what host to 'reflect' api from") 
@click.option('-p', '--port', default=5000, help="This should include what port to 'reflect' api from")
@click.argument('user_id')
@click.argument('snapshot_id')
def get_snapshot(host,port,user_id,snapshot_id):
	'''Returns the specified snapshot's details: ID, datetime, and the available results' names only. '''
	api_server_url = f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}'
	response = requests.get(api_server_url)
	print(response.json())

@cli.command('get-result')
@click.option('-h', '--host', default='127.0.0.1', help="This should include what host to 'reflect' api from") 
@click.option('-p', '--port', default=5000, help="This should include what port to 'reflect' api from")
@click.argument('user_id')
@click.argument('snapshot_id')
@click.argument('result_name')
@click.option('-s', '--save', default=None, help="If this flag is specified, then it saves the data to the given path")
def get_result(host,port, user_id,snapshot_id, result_name, save):
	'''Returns the specified snapshot's results. Saves it if given path. '''
	api_server_url = f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result_name}'
	response = requests.get(api_server_url)
	output = response.json()
	if save is not None:
		with open(save, 'w') as f:
			json.dump(output, f)
	print(output)




cli()
