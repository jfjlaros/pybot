from psycopg2 import *

_original_connect = connect

def connect(*args, **kwargs):
    kwargs.pop("unicode_results")
    return _original_connect(*args, **kwargs)
