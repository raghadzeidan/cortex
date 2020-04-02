

AVAILABLE_PARSERS = set()
def subscribe(parser_name):
    def decorator(f):
        AVAILABLE_PARSERS.add(parser_name)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs) #function behaves like the real function.
        return wrapper
    return decorator
