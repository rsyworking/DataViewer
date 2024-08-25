import inspect
from datetime import datetime

def time_delta(func):
    def wrapper(*args, **kwargs):
        FMT = '%H:%M:%S'
        print("Something is happening before the function is called.")
        start_time = datetime.now()
        func(*args, **kwargs)
        end_time = datetime.now()
        _time_delta = end_time - start_time
        print(f'Time spent: {_time_delta} to run: {func}')
    return wrapper

def inspect_func(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        members = inspect.getmembers(func)
        print( members)
    return wrapper