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

