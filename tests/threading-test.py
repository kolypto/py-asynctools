import unittest
import time

from asynctools.threading import Async, Parallel, Pool
from asynctools._testutil import timeit


class AsyncTest(unittest.TestCase):
    def setUp(self):
        self._result = None

    @Async
    def _w_sleep(self, sleep):
        """ Worker that sleeps """
        time.sleep(sleep)
        self._result = sleep

    def test_async(self):
        """ Run 3 tasks, don't wait """
        t = timeit()
        map(self._w_sleep, (0.1, 0.5, 0.8))
        self.assertAlmostEqual(0.0, t(), delta=0.1)

    def test_async_wait(self):
        """ Run 3 tasks, see it they manage to modify a property """
        self.test_async()
        time.sleep(1)
        self.assertEqual(self._result, 0.8)

    def test_async_wait_event(self):
        """ Run a task, wait() for it """
        t = timeit()
        self._w_sleep(0.5).wait()
        self.assertAlmostEqual(0.5, t(), delta=0.1)


class ParallelTest(unittest.TestCase):
    """ Test: Parallel """
    Cls = lambda self, worker: Parallel(worker)

    def _w_smallsleep(self, sleep):
        """ Worker that sleeps. If sleep >= 1 -- fail """
        assert sleep < 1
        time.sleep(sleep)
        return sleep

    test_join_expected_runtime = 0.8
    def test_join(self):
        """ Test with 3 sleeps """
        pll = self.Cls(self._w_smallsleep)
        times = [0.2, 0.5, 0.8]
        map(pll, times)

        # Should finish quick
        t = timeit()
        results, errors = pll.join()
        self.assertAlmostEqual(self.test_join_expected_runtime, t(), delta=0.1)

        # Results
        self.assertEqual(results, times)
        self.assertEqual(errors, [])

    test_join_reversed_expected_runtime = 0.8
    test_join_reversed_expected_results = [0.2, 0.5, 0.8]
    def test_join_reversed(self):
        times = [0.8, 0.2, 0.5]
        t = timeit()
        results, errors = self.Cls(self._w_smallsleep).map(times).join()

        # Should have the same results
        self.assertAlmostEqual(self.test_join_reversed_expected_runtime, t(), delta=0.1)
        self.assertEqual(results, self.test_join_reversed_expected_results)  # Still same order
        self.assertEqual(errors, [])

    test_join_with_errors_expected_runtime = 0.8
    def test_join_with_errors(self):
        """ Test with 3 sleeps and 1 error """
        pll = self.Cls(self._w_smallsleep)
        times = [0.2, 0.5, 0.8, 2]  # 2 will cause an error
        pll.map(times)

        # Should finish quick
        t = timeit()
        results, errors = pll.join()
        self.assertAlmostEqual(self.test_join_with_errors_expected_runtime, t(), delta=0.1)

        # Results
        self.assertEqual(results, times[:-1])
        # Error should be caught
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], AssertionError)

    test_join_errors_expected_runtime = 0.0
    def test_join_errors(self, expected_runtime=0.0):
        """ Test with 3 errors """
        pll = self.Cls(self._w_smallsleep)
        times = [2, 3, 4]  # Only errors
        pll.map(times)

        # Should finish quick
        t = timeit()
        results, errors = pll.join()
        self.assertAlmostEqual(self.test_join_errors_expected_runtime, t(), delta=0.1)  # No sleeps: extremely quick

        # Results
        self.assertEqual(results, [])
        # Error should be caught
        self.assertEqual(len(errors), 3)
        self.assertIsInstance(errors[0], AssertionError)
        self.assertIsInstance(errors[1], AssertionError)
        self.assertIsInstance(errors[2], AssertionError)

    test_first_expected_runtime = 0.2
    test_first_expected_result = 0.2
    def test_first(self):
        """ Test with 3 sleeps: first """
        t = timeit()
        result = self.Cls(self._w_smallsleep).map([0.8, 0.5, 0.2]).first()
        self.assertEqual(result, self.test_first_expected_result)
        self.assertAlmostEqual(self.test_first_expected_runtime, t(), delta=0.1)

    def test_first_with_errors(self):
        """ Test with 1 error and 3 sleeps: second """
        t = timeit()
        result = self.Cls(self._w_smallsleep).map([2, 0.5, 0.2]).first()
        self.assertEqual(result, 0.2)
        self.assertAlmostEqual(0.2, t(), delta=0.1)

    def test_first_errors(self):
        """ Test with 3 errors: none """
        t = timeit()
        result = self.Cls(self._w_smallsleep).map([2, 3, 4]).first()
        self.assertEqual(result, None)
        self.assertAlmostEqual(0.0, t(), delta=0.1)

class PoolTest(ParallelTest):
    """ Test: Pool """
    Cls = lambda self, worker: Pool(worker, 2)
    test_join_expected_runtime = 1.0
    test_join_reversed_expected_runtime = 0.8
    test_join_reversed_expected_results = [0.2, 0.5, 0.8]
    test_join_with_errors_expected_runtime = 1.0
    test_join_errors_expected_runtime = 0.0
    test_first_expected_runtime = 0.5
    test_first_expected_result = 0.5

    def test_twice(self):
        """ Test two sets of tasks """
        pool = Pool(self._w_smallsleep, 2)

        # First set of tasks
        pool.map([0.1, 0.5, 0.8])
        t = timeit()
        results, errors = pool.join()
        self.assertAlmostEqual(0.9, t(), delta=0.1)
        self.assertEqual((len(results), len(errors)), (3, 0))

        # Second set of tasks: pool still working
        pool.map([0.1, 0.5, 0.8])
        t = timeit()
        pool.join()
        self.assertAlmostEqual(0.9, t(), delta=0.1)
        self.assertEqual((len(results), len(errors)), (3, 0))

        # 2 Threads
        self.assertEqual(len(pool._threads), 2)

        # Finish
        pool.close()

        # Cannot use
        self.assertRaises(RuntimeError, pool, 1)
        self.assertRaises(RuntimeError, pool.join)
