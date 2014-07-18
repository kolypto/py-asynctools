from threading import Thread, Condition
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
        self._results, self._errors = [], []
        self._jobfinished = Condition()

    def _spawn_thread(self, target):
        """ Create a thread """
        t = Thread(target=target)
        t.daemon = True
        t.start()
        return t

    def _add_job(self, args, kwargs):
        self._jobs.put((args, kwargs))

    def _terminate_one_thread(self):
        """ Put (None,None) in the queue, which is the thread termination signal """
        self._add_job(None, None)

    def _thread(self):
        """ Thread entry point: does the job once, stored results, and dies. """
        # Get
        args, kwargs = self._jobs.get()

        # Stop thread when (None, None) comes in
        if args is None and kwargs is None:
            return None  # Wrappers should exit as well

        # Work
        try:
            self._results.append(self._worker(*args, **kwargs))
            return True
        except Exception as e:
            self._errors.append(e)
            return False
        finally:
            self._jobs.task_done()
            with self._jobfinished:
                self._jobfinished.notify()

    def map(self, jobs):
        map(self, jobs)
        return self

    def __call__(self, *args, **kwargs):
        """ Add a job. Arguments are directly passed to the worker """
        self._add_job(args, kwargs)
        if self._class == 'Parallel':
            self._spawn_thread(self._thread)
        return self

    def first(self, timeout=None):
        """ Wait for the first successful result to become available
        :param timeout: Wait timeout, sec
        :type timeout: float|int|None
        :return: result, or None if all threads have failed
        :rtype: *
        """
        while True:
            with self._jobfinished:
                if self._results or not self._jobs.unfinished_tasks:
                    break
                self._jobfinished.wait(timeout)
        return self._results[0] if self._results else None

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
