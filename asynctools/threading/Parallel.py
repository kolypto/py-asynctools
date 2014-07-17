from threading import Thread, Event
from Queue import Queue


class Parallel(object):
    """ Execute all tasks in parallel, once """
    _class = 'Parallel'

    def __init__(self, worker):
        """ Initialize threaded executor with a worker function
            :param worker: A function to process a single job. Arguments are passed from :meth:Once.job
            :type worker: callable
        """
        self._worker = worker
        self._jobs = Queue()
        self._results = []
        self._errors = []

    def _spawn_thread(self, target):
        """ Create a thread """
        t = Thread(target=target)
        t.daemon = True
        t.start()
        return t

    def _terminate_thread(self):
        """ Put (None,None) in the queue, which is the thread termination signal """
        self._jobs.put((None, None))  # Termination signal

    def _worker_once(self):
        """ Worker wrapper that stores results """
        # Get
        args, kwargs = self._jobs.get()

        # Stop thread when (None, None) comes in
        if args is None and kwargs is None:
            return False  # Top-level loopers should exit as well

        # Work
        try:
            self._results.append(self._worker(*args, **kwargs))
        except Exception as e:
            self._errors.append(e)
        finally:
            self._jobs.task_done()

    def job(self, *args, **kwargs):
        """ Add a job. Arguments are directly passed to the worker """
        self._jobs.put((args, kwargs))

        # Spawn a thread if needed
        if self._class == 'Parallel':
            self._spawn_thread(self._worker_once)

    def join(self):
        """ Wait for all current tasks to be finished """
        self._jobs.join()
        try:
            return self._results, self._errors
        finally:
            self._clear()

    def _clear(self):
        self._results = []
        self._errors = []
