import click
import thought_server

@click.group()
def main():
    pass

@main.command('upload_thought')
@click.argument('address') # help='the first arguemnt should be the address, consisting of an IP address and a port seperated by a \':\'')
@click.argument('user_id') # help = 'this should be the user\'s ID')
@click.argument('thought') # help = 'this is the thought(noun) that the user thought(verb)')
def main_upload_thought(address, user_id, thought):
    thought_server.upload_thought(address, user_id, thought)

@main.command('run_webserver')
@click.argument('address') # help='the first arguemnt should be the address, consisting of an IP address and a port seperated by a \':\'')
@click.argument('data_directory') # help='this should be the path to the directory that is going to store the messages')
def main_run_webserver(address, data_directory):
    thought_server.run_webserver(address, data_directory)

@main.command('run_server')
@click.argument('address') # help='the first arguemnt should be the address, consisting of an IP address and a port seperated by a \':\'')
@click.argument('data_directory') # help='this should be the path to the directory that is going to store the messages')
def main_run_server(address, data_directory):
    thought_server.run_server(address, data_directory)


main()
