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
        self._threads = [ self._spawn_thread(self._worker_forever) for i in range(0, size) ]

    def _worker_forever(self):
        """ Worker that continuously fetches tasks """
        while self._worker_once() is not False: pass

    def close(self):
        # Terminate threads
        for t in self._threads:
            self._terminate_thread()
        self._threads = []

        # Seal
        self.job = self.join = self.first = self._closed

    __enter__ = lambda self: None
    __exit__ = close

    def _closed(self, *args, **kwargs):
        raise RuntimeError('Cannot use a closed pool')
