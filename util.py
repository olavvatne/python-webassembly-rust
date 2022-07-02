import time


def timethis(func):
    def wrapper(*args, **kwards):
        start = time.perf_counter()
        retval = func(*args, **kwards)
        stop = time.perf_counter()
        print("time s", stop - start)
        return retval
    return wrapper