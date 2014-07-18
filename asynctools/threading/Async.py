from threading import Thread, Event
from functools import wraps, partial

# def Async(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         t = Thread(target=func, args=args, kwargs=kwargs)
#         t.daemon = True
#         t.start()
#     return wrapper


class Async(object):
    """ Decorator for functions that should be run in a thread """

    def __init__(self, func):
        self._func = func

    def _thread(self, event, args, kwargs):
        try: self._func(*args, **kwargs)
        finally: event.set()

    def __get__(self, obj, type=None):  # Descriptor
        return partial(self, obj)

    def __call__(self, *args, **kwargs):
        """ Launch the function in a thread and return an event.
        :rtype: Event
        """
        event = Event()
        t = Thread(target=self._thread, args=(event, args, kwargs))
        t.daemon = True
        t.start()
        return event
