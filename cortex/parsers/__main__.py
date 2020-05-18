from .color_image_parser import color_image_parser_main
from .feelings_parser import feelings_parser_main
from .pose_parser import pose_parser_main
from .depth_image_parser import depth_image_parser_main
from .parsers_main import run_parser
import click

@click.group()
def cli():
    pass

#@cli.command('parse')
#@click.argument('parser_name', help = 'this should have the parser name that we want to parse this specific data using')
#@click.argument('data', 'this should have the data that we want to parse')
#@click.option('redirect', 'this is optional, if you want to redirect the data to a specific file')
#def parse(parser_name, data_path, redirect=None):#this shit is temporaray, this should call to other function defined in main parser function in parser package
#	pass
#    with open(data_path,'r') as f:
#		data = run_parser(f.read())
#	if redirect:
#		with open(redirect, 'w') as f:
#			f.write(data)
#	else:
#		print(data)

@cli.command('run-parser')
@click.argument('parser_name')#,help='this should have the parser name that we want to parse this specific data using')
@click.argument('mq')
def microservice_run_parser(parser_name, mq):#this shit is temporaray, this should call to other function defined in main parser function in parser package
	print(mq)
	print(parser_name)
	if parser_name == 'feelings':
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
