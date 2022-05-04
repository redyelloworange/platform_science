import primefac
from typing import Dict


class FactorCache(object):
    def __init__(
            self,
            memoized_prime_factors_by_int: Dict[int, int]=None):
        if memoized_prime_factors_by_int is None:
            memoized_prime_factors_by_int = {}
        self._memoized_prime_factors_by_int = \
            memoized_prime_factors_by_int

    def get_prime_factors_by_int(self, n: int):
        if n not in self._memoized_prime_factors_by_int:
            self._memoized_prime_factors_by_int[n] = \
                set([x for x in primefac.primefac(n)])
        return self._memoized_prime_factors_by_int[n]

    def get_prime_factors_by_name(self, name: str):
        return self.get_prime_factors_by_int(len(name))
