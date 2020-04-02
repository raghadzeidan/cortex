from .color_image_parser import parse_that_fucking_image
import click

@click.command('parse_image')
@click.argument('image') # help='the first arguemnt should be the address, consisting of an IP address and a port seperated by a \':\'')
def main_parse_image(image):
    parse_that_fucking_image(image)

print("hi")
