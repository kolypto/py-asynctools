from . import Parallel


class Pool(Parallel):
    """ Execute all tasks in a parallel pool """
    _class = 'Pool'

    def __init__(self, worker, size):
        """ Initialize threaded executor with a worker function
            :param worker: A function to process a single job. Arguments are passed from :meth:Once.job
            :type worker: callable
        """
        super(Pool, self).__init__(worker)

        # Spawn threads
        self._threads = [ self._spawn_thread(self._thread) for i in range(0, size) ]

    def _thread(self):
        """ Worker that continuously fetches tasks """
        while super(Pool, self)._thread() is not None: pass

    def close(self):
        # Terminate threads
        for t in self._threads:
            self._terminate_one_thread()
        self._threads = []

        # Seal
        self._add_job = self.join = self._closed

    __enter__ = lambda self: None
    __exit__ = close

    @staticmethod
    def _closed(*args, **kwargs):
        raise RuntimeError('Cannot use a closed pool')
