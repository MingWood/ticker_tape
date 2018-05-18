
REGISTERED_ALGORITHMS = {}


def retrieve_algorithms():
    from .. import algorithms
    return REGISTERED_ALGORITHMS


def register_algorithm(func):
    REGISTERED_ALGORITHMS[func.__name__] = func
    return func
