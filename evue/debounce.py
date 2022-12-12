# -*- coding: utf-8 -*-
import functools
from threading import Timer
from typing import Callable

class debounce:  # noqa
    def __init__(self, timeout: float = 1):
        self.timeout = timeout
        self._timer = None

    def __call__(self, func: Callable):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            if self._timer is not None:
                self._timer.cancel()
            self._timer = Timer(self.timeout, func, args=args, kwargs=kwargs)
            self._timer.start()

        return decorator