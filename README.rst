AsyncTools
==========

Async Tools for Python.

Threading
---------

Threading is the most simple thing, but because of
`GIL <https://wiki.python.org/moin/GlobalInterpreterLock>`__ it's
useless for computation. Only use when you want to parallelize the
access to a blocking resource, e.g. network.

Parallel
--------

Source:
`asynctools/threading/Parallel.py <asynctools/threading/Parallel.py>`__

Execute functions in parallel and collect results. Each function is
executed in its own thread, all threads exit immediately.

Methods:

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
        pll.job(url)  # Starts a new thread
        
        
    # Wait for the results
    results, errors = pll.join()

Pool
----

Source: `asynctools/threading/Pool.py <asynctools/threading/Pool.py>`__

Create a pool of threads and execute work in it. Useful if you do want
to launch a limited number of long-living threads.

Methods:

-  ``join()``: Wait for all tasks to be finished and return
   ``(results, errors)`` (same as with ```Pool`` <#pool>`__)
-  ``close()``: Terminate all threads.
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
        pll.job(url)  # Runs in a pool

    # Wait for the results
    results, errors = pll.join()

