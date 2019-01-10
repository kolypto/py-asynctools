`Build Status <https://travis-ci.org/kolypto/py-asynctools>`__
`Pythons <.travis.yml>`__

AsyncTools
==========

Async Tools for Python.

Table of Contents
=================

-  Threading

   -  Async
   -  Parallel
   -  Pool

Threading
=========

In Python, threading only makes sense to run blocking calls
concurrently: e.g. accessing network resources. Threading is useless for
computations because of
`GIL <https://wiki.python.org/moin/GlobalInterpreterLock>`__.

Async
-----

Source:
`asynctools/threading/Async.py <asynctools/threading/Async.py>`__

Decorator for functions that should be run in a separate thread. When
the function is called, it returns a
```threading.Event`` <https://docs.python.org/2/library/threading.html#event-objects>`__.

.. code:: python

   from asynctools.threading import Async

   @Async
   def request(url):
       # ... do request
       
   request('http://example.com')  # Async request
   request('http://example.com').wait()  # wait for it to complete

If you want to wait for multiple threads to complete, see next chapters.

Parallel
--------

Source:
`asynctools/threading/Parallel.py <asynctools/threading/Parallel.py>`__

Execute functions in parallel and collect results. Each function is
executed in its own thread, all threads exit immediately.

Methods:

-  ``__call__(*args, **kwargs)``: Add a job. Call the ``Parallel``
   object so it calls the worker function with the same arguments
-  ``map(jobs)``: Convenience method to call the worker for every
   argument
-  ``first(timeout=None)``: Wait for a single result to be available,
   with an optional timeout in seconds. The result is returned as soon
   as it’s ready. If all threads fail with an error – ``None`` is
   returned.
-  ``join()``: Wait for all tasks to be finished, and return two lists:

   -  A list of results
   -  A list of exceptions

Example:

.. code:: python

   from asynctools.threading import Parallel

   def request(url):
       # ... do request
       return data
      
   # Execute
   pll = Parallel(request)
   for url in links:
       pll(url)  # Starts a new thread
       
       
   # Wait for the results
   results, errors = pll.join()

Since the request method takes just one argument, this can be chained:

.. code:: python

   results, errors = Parallel(request).map(links).join()

Pool
----

Source: `asynctools/threading/Pool.py <asynctools/threading/Pool.py>`__

Create a pool of threads and execute work in it. Useful if you do want
to launch a limited number of long-living threads.

Methods are same with ```Parallel`` <#parallel>`__, with some additions:

-  ``__call__(*args, **kwargs)``
-  ``map(jobs)``
-  ``first(timeout=None)``
-  ``close()``: Terminate all threads. The pool is no more usable when
   closed.
-  ``__enter__``, ``__exit__`` context manager to be used with ``with``
   statement

Example:

.. code:: python

   from asynctools.threading import Pool

   def request(url):
       # ... do long request
       return data
      
   # Make pool
   pool = Pool(request, 5)

   # Assign some job
   for url in links:
       pll(url)  # Runs in a pool

   # Wait for the results
   results, errors = pll.join()
