# -*- coding: utf-8 -*-
from __future__ import print_function
import threading
import atexit


def test():
    """Test function. Prints "Hello World". Returns None"""
    print ("Hello World")
    
def noop():
    """Test function. Does nothing."""
    pass

# Contains a list of active timeouts
timeouts = {}
# Contains a list of active intervals
intervals = {}

# Internally used counters.
_interval_ctr = 0
_timeout_ctr = 0

def _new_interval_id():
    """Used internally to return the next available interval ID."""
    global _interval_ctr
    _interval_ctr += 1
    return _interval_ctr

def _new_timeout_id():
    """Used internally to return the next available timeout ID."""
    global _timeout_ctr
    _timeout_ctr += 1
    return _timeout_ctr

def setTimeout(f, delay, *args, **kwargs):
    """Creates a Timer event that runs the function 'f' after 'delay' (in milliseconds) duration.
    
    f: function to be called
    delay: time in milliseconds after which f will be called.
    [args,kwargs]: Parameters to be passed to the function 'f' on call.
    
    Returns: Timeout ID. Used by clearTimeout() to clear the timeout.
    """
    t_id = _new_timeout_id()
    def f_major():
        f(*args, **kwargs)
        try:
            del timeouts[t_id]
        except KeyError:
            pass
    t = threading.Timer(1.0*delay/1000,f_major)
    timeouts[t_id] = t
    t.daemon = True
    t.start()
    return t_id

def setInterval(f,delay, *args, **kwargs):
    """Creates a Timer event that runs the function 'f' every 'delay' milliseconds till cancelled.
    
    f: function to be called
    delay: time in milliseconds after which f will be repeatedly called.
    [args,kwargs]: Parameters to be passed to the function 'f' on call.
    
    Returns: Interval ID. Used by clearInterval() to clear the interval.
    """
    i_id = _new_interval_id()
    def f_major():
        f(*args, **kwargs)
        t = threading.Timer(1.0*delay/1000,f_major)
        intervals[i_id] = t
        t.daemon = True
        t.start()
    t = threading.Timer(1.0*delay/1000,f_major)
    intervals[i_id] = t
    t.daemon = True
    t.start()
    return i_id

def clearInterval(i_id):
    """Cancels the Interval event with the specified ID."""
    try:
        intervals[i_id].cancel()
        del intervals[i_id]
        return 0
    except KeyError:
        return 1

def clearTimeout(t_id):
    """Cancels the Timeout event with the specified ID."""
    try:
        timeouts[t_id].cancel()
        del timeouts[t_id]
        return 0
    except KeyError:
        return 1

@atexit.register
def clearAll():
    """Clears all intervals/timeouts. Runs on exit."""
    for i_id in list(intervals):
        clearInterval(i_id)
    for t_id in list(timeouts):
        clearTimeout(t_id)

if __name__ == "__main__":
    print ("""Usage:
        
    import jstimers
    
    i_id = jstimers.setInterval(jstimers.test, 2000)
    jstimers.clearInterval(i_id)
    """)