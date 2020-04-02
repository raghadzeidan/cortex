from .client import upload_sample
import click

@click.group()
def main():
    pass

@main.command('upload-sample')
@click.option('-h' ,'--host', default='127.0.0.1', help = "this should be the host ip in which the clients sends data to" ) 
@click.option('-p', '--port', default = 8000, help = 'this should  be the port in which the client sends data to') 
@click.argument('sample')
def main_upload(host, port, sample):
    upload_sample(host, port, sample)


main()
