AVAILABLE_PARSERS = set()
def subscribe(parser_name):
    '''this functions allows parsers to enroll in an AVAILABLE_PARSERS set
    which is then used by the server, to publish back to clients indicating
    which parsing functionalities are available for us. exactly those which
    are implemented.'''
    def decorator(f):
        AVAILABLE_PARSERS.add(parser_name)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs) #function behaves like the real function.
        return wrapper
    return decorator


def run_parser(parser_name, data):
    '''this should return the result of the parsing on the data'''
    if parser_name not in AVAILABLE_PARSERS:
        raise TypeError('parser not suppeoted')
    if parser_name == 'feelings':
        return parse_those_fucking_feelings(data)
    if parser_name == 'color_image':
        return parse_that_fucking_image(data)
