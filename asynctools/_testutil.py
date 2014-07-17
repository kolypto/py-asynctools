""" Unit-test utilities """

from datetime import datetime

class timeit(object):
    """ Measure execution time """
    def __init__(self):
        self.start = datetime.utcnow()

    def __call__(self):
        t = datetime.utcnow()
        return (t - self.start).total_seconds()
