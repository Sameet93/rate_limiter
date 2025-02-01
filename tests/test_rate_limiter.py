import time
import unittest
import logging
from rate_limiter.caches import MemoryCache
from rate_limiter.rate_limiter import rate_limit

# Configure logging to display debug messages during tests.
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class TestMemoryCache(unittest.TestCase):
    def setUp(self):
        self.cache = MemoryCache()
        logging.debug("Set up MemoryCache for TestMemoryCache.")

    def test_set_and_get(self):
        logging.debug("Starting test_set_and_get")
        self.cache.set("key1", "value1", expire=2)
        logging.debug("Set key1 to 'value1' with 2 sec expiration.")
        self.assertEqual(self.cache.get("key1"), "value1")
        logging.debug("Retrieved key1 successfully before expiration.")
        time.sleep(2.1)
        logging.debug("Waited 2.1 seconds for key1 to expire.")
        self.assertIsNone(self.cache.get("key1"))
        logging.debug("Confirmed key1 has expired.")

    def test_incr(self):
        logging.debug("Starting test_incr")
        first = self.cache.incr("counter", expire=2)
        logging.debug(f"First increment: {first}")
        self.assertEqual(first, 1)
        second = self.cache.incr("counter", expire=2)
        logging.debug(f"Second increment: {second}")
        self.assertEqual(second, 2)
        time.sleep(2.1)
        logging.debug("Waited 2.1 seconds for counter to expire.")
        third = self.cache.incr("counter", expire=2)
        logging.debug(f"Third increment after expiration: {third}")
        self.assertEqual(third, 1)

    def test_ban(self):
        logging.debug("Starting test_ban")
        self.cache.ban("user1", ban_duration=2)
        logging.debug("Banned user1 for 2 seconds.")
        self.assertTrue(self.cache.is_banned("user1"))
        logging.debug("Confirmed user1 is banned.")
        time.sleep(2.1)
        logging.debug("Waited 2.1 seconds for ban to expire.")
        self.assertFalse(self.cache.is_banned("user1"))
        logging.debug("Confirmed user1 ban has expired.")

class TestRateLimiterDecorator(unittest.TestCase):
    def setUp(self):
        self.cache = MemoryCache()
        logging.debug("Set up MemoryCache for TestRateLimiterDecorator.")

    def dummy_function(self):
        logging.debug("dummy_function called.")
        return "Success!"

    def test_rate_limit_within_limit(self):
        logging.debug("Starting test_rate_limit_within_limit")
        limited_func = rate_limit(limit=3, period=2, identifier=lambda: "user1", cache=self.cache)(self.dummy_function)
        logging.debug("Calling limited_func three times within the limit.")
        self.assertEqual(limited_func(), "Success!")
        logging.debug("First call succeeded.")
        self.assertEqual(limited_func(), "Success!")
        logging.debug("Second call succeeded.")
        self.assertEqual(limited_func(), "Success!")
        logging.debug("Third call succeeded.")

    def test_rate_limit_exceeded(self):
        logging.debug("Starting test_rate_limit_exceeded")
        limited_func = rate_limit(limit=3, period=2, identifier=lambda: "user2", cache=self.cache)(self.dummy_function)
        logging.debug("Calling limited_func three times to reach the limit.")
        limited_func()
        limited_func()
        limited_func()
        logging.debug("Reached limit; attempting a fourth call to exceed the limit.")
        with self.assertRaises(Exception) as context:
            limited_func()
        self.assertIn("Rate limit exceeded", str(context.exception))
        logging.debug("Caught expected exception: 'Rate limit exceeded'.")

    def test_auto_ban_after_threshold(self):
        logging.debug("Starting test_auto_ban_after_threshold")
        limited_func = rate_limit(
            limit=3,
            period=2,
            identifier=lambda: "user3",
            cache=self.cache,
            auto_ban=True,
            ban_threshold=4,  # Ban if the count exceeds 4.
            ban_duration=2
        )(self.dummy_function)
        
        logging.debug("Calling limited_func three times within limit for auto-ban test.")
        self.assertEqual(limited_func(), "Success!")
        logging.debug("Call 1 succeeded.")
        self.assertEqual(limited_func(), "Success!")
        logging.debug("Call 2 succeeded.")
        self.assertEqual(limited_func(), "Success!")
        logging.debug("Call 3 succeeded.")
        
        logging.debug("Calling limited_func 4th time (should exceed limit).")
        with self.assertRaises(Exception) as context1:
            limited_func()  # count = 4
        self.assertIn("Rate limit exceeded", str(context1.exception))
        logging.debug("4th call correctly raised 'Rate limit exceeded'.")
        
        logging.debug("Calling limited_func 5th time (should trigger auto-ban).")
        with self.assertRaises(Exception) as context2:
            limited_func()  # count = 5, auto-ban triggered
        self.assertIn("Rate limit exceeded", str(context2.exception))
        logging.debug("5th call correctly triggered auto-ban with 'Rate limit exceeded'.")
        
        logging.debug("Calling limited_func 6th time (should immediately detect ban).")
        with self.assertRaises(Exception) as context_ban:
            limited_func()  # now banned
        self.assertIn("temporarily banned", str(context_ban.exception))
        logging.debug("6th call correctly raised 'temporarily banned'.")

if __name__ == '__main__':
    unittest.main()
