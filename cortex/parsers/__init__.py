print('inside __init__ of parsers')
from .parsers_main import AVAILABLE_PARSERS
from .feelings_parser import parse_those_fucking_feelings
from .color_image_parser import parse_that_fucking_image
from .depth_image_parser import parse_that_fucking_depth
from .pose_parser import parse_that_fucking_pose

def run_parser(parser_name, data):
	'''this should return the result of the parsing on the data 
	HOW TO ADD PARSER: 
	In order to add a new parser, a number of functions/modules have to be implemented. for example smell_parser:
	1: you have to create a new module with the parser's name inside parsers directory. example: smell_parser.py
	2: you have to implemente a parsing function, that does the processing of smell, noteably they're called "fucking" function: example: parse_that_fucking_smell
	3: the function above should be decorated with a subscribe('smell') decorator, to add it to the list of the server's parsers that he receives from clients
	3.25: you should implement the relevant MQ (RabbitMQ in our case) callback function, in order to decouple it from the parsing function itself.
	3.5: you should implement a main function inside your module, to process MQ information and decouple the processing function from it.
	4: in order to expose your module to the rest of the program, you must import it in the __init__.py of parsers package
	5: (optoinal) to suppprt usage of parser in the run_parser function, you must add an if-clause with the parser's
	   name, simiilar to how other parsers are done.'''
	
	if parser_name not in AVAILABLE_PARSERS:
		raise TypeError('parser not supperted')
	if parser_name == 'feelings':
		return parse_those_fucking_feelings(data)
	if parser_name == 'color_image':
		return parse_that_fucking_image(data)
	if parser_name == 'depth_image':
		return parse_that_fucking_depth(data)
	if parser_name == 'pose':
		return parse_that_fucking_pose(data)
	raise TypeError('parser supported but does not support this way of using it.')
