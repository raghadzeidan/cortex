from .server import run_server
import click
@click.group()
def main():
    pass

@main.command('run-server')
@click.argument('host') # help='the first arguemnt should be the address, consisting of an IP address and a port seperated by a \':\'')
@click.argument('port') # help = 'this should be the user\'s ID')
def main_run_server(host, port):
    run_server(host, port)
