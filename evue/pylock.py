# -*- coding: utf-8 -*-
import threading

mutex = threading.Lock()

def lock(func):
    def wrapper(*args, **kwargs):
        with mutex:
            ret = func(*args, **kwargs)
        return ret
    return wrapper
