import .client as client


@click.group()
def main():
    pass

@main.command('upload-sample')
@click.argument('host') # help='the first arguemnt should be the address, consisting of an IP address and a port seperated by a \':\'')
@click.argument('port') # help = 'this should be the user\'s ID')
@click.argument('sample') # help = 'this is the thought(noun) that the user thought(verb)')
def main_upload-sample(host, port, sample):
    client.upload_sample(host, port, sample)
