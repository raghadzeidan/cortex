from .color_image_parser import color_image_parser_main
from .feelings_parser import feelings_parser_main
from .pose_parser import pose_parser_main
from .depth_image_parser import depth_image_parser_main
from . import run_parser
import click

@click.group()
def cli():
    pass

@cli.command('parse')
@click.option('--redirect', default=None, help='this is optional, if you want to redirect the data to a specific file')
@click.argument('parser_name')
@click.argument('data')
def parse(parser_name, data_path, redirect):
	with open(data_path,'r') as f:
		data = run_parser(f.read())
	if redirect is not None:
		with open(redirect, 'w') as f:
			f.write(data)
	else:
		print(data)

@cli.command('run-parser')
@click.argument('parser_name')
@click.argument('mq')
def microservice_run_parser(parser_name, mq):
	print(mq)
	print(parser_name)
	if parser_name == 'feelings':
		print("inside feelings")
		feelings_parser_main(mq)
	elif parser_name == 'color_image':
		color_image_parser_main(mq)
	elif parser_name == 'depth_image':
		depth_image_parser_main(mq)
	elif parser_name == 'pose':
		pose_parser_main(mq)
	else:
		raise TypeError('Unsuppored/invalid parser name')
		


cli()
