import unittest
import time

from asynctools.threading import Parallel, Pool
from asynctools._testutil import timeit


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
        map(pll.job, times)

        # Should finish quick
        t = timeit()
        results, errors = pll.join()
        self.assertAlmostEqual(self.test_join_expected_runtime, t(), delta=0.1)

        # Results
        self.assertEqual(results, times)
        self.assertEqual(errors, [])

    test_join_with_errors_expected_runtime = 0.8
    def test_join_with_errors(self):
        """ Test with 3 sleeps and 1 error """
        pll = self.Cls(self._w_smallsleep)
        times = [0.2, 0.5, 0.8, 2]  # 2 will cause an error
        map(pll.job, times)

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
        map(pll.job, times)

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


class PoolTest(ParallelTest):
    """ Test: Pool """
    Cls = lambda self, worker: Pool(worker, 2)
    test_join_expected_runtime = 1.0
    test_join_with_errors_expected_runtime = 1.0
    test_join_errors_expected_runtime = 0.0
    test_first_expected_runtime = 0.1

    def test_twice(self):
        """ Test two sets of tasks """
        pool = Pool(self._w_smallsleep, 2)

        # First set of tasks
        map(pool.job, [0.1, 0.5, 0.8])
        t = timeit()
        results, errors = pool.join()
        self.assertAlmostEqual(0.9, t(), delta=0.1)
        self.assertEqual((len(results), len(errors)), (3, 0))

        # Second set of tasks: pool still working
        map(pool.job, [0.1, 0.5, 0.8])
        t = timeit()
        pool.join()
        self.assertAlmostEqual(0.9, t(), delta=0.1)
        self.assertEqual((len(results), len(errors)), (3, 0))

        # 2 Threads
        self.assertEqual(len(pool._threads), 2)

        # Finish
        pool.close()

        # Cannot use
        self.assertRaises(RuntimeError, pool.job, 1)
