from factor_cache import FactorCache
from unittest import TestCase


class TestFactorCache(TestCase):
    def setUp(self):
        self._factor_cache = FactorCache()

    def test_get_factors_by_int(self):
        self.assertSetEqual(
            set([2, 3]),
            self._factor_cache.get_prime_factors_by_int(36))

    def test_get_factors_by_name(self):
        self.assertSetEqual(
            set([3, 5]),
            self._factor_cache.get_prime_factors_by_name('St. James Place'))
