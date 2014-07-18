[![Build Status](https://api.travis-ci.org/kolypto/py-asynctools.png?branch=master)](https://travis-ci.org/kolypto/py-asynctools)


AsyncTools
==========

Async Tools for Python.

Table of Contents
=================

* <a href="#user-content-threading">Threading</a>
    * <a href="#user-content-parallel">Parallel</a>
    * <a href="#user-content-pool">Pool</a> 

Threading
=========

Threading is the most simple thing, but because of [GIL](https://wiki.python.org/moin/GlobalInterpreterLock) it's useless for computation.
Only use when you want to parallelize the access to a blocking resource, e.g. network.

Parallel
--------

Source: [asynctools/threading/Parallel.py](asynctools/threading/Parallel.py)

Execute functions in parallel and collect results.
Each function is executed in its own thread, all threads exit immediately.

Methods:

* `__call__`: Add a job. Call the `Parallel` object so it calls the worker function with the same arguments
* `map(jobs)`: Convenience method to call the worker for every argument
* `join()`: Wait for all tasks to be finished, and return two lists:
    
    * A list of results
    * A list of exceptions

Example:

```python
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
```

Since the request method takes just one argument, this can be chained:

```python
results, errors = Parallel(request).map(links).join()
```



Pool
----

Source: [asynctools/threading/Pool.py](asynctools/threading/Pool.py)

Create a pool of threads and execute work in it.
Useful if you do want to launch a limited number of long-living threads.

Methods:

* `join()`: Wait for all tasks to be finished and return `(results, errors)` (same as with [`Pool`](#pool))
* `close()`: Terminate all threads. The pool is no more usable when closed.
* `__enter__`, `__exit__` context manager to be used with `with` statement

Example:

```python
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
```
