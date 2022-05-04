from typing import Dict, Tuple

from src.character_evaluation import is_vowel, is_consonant
from src.factor_cache import FactorCache


def calculate_base_suitability_score_even_destination(
        driver_name: str, street_name: str):
    assert (len(street_name) % 2 == 0)
    return 1.5 * len(
        [c
         for c
         in driver_name
         if is_vowel(c)])


def calculate_base_suitability_score_odd_destination(
        driver_name: str, street_name: str):
    assert (len(street_name) % 2 == 1)
    return 1.5 * len(
        [c
         for c
         in driver_name
         if is_consonant(c)])


def calculate_base_suitability_score(driver_name: str, street_name: str):
    if len(street_name) % 2 == 0:
        return calculate_base_suitability_score_even_destination(
            driver_name, street_name)
    else:
        return calculate_base_suitability_score_odd_destination(
            driver_name, street_name)


class SuitabilityScoreCalculator(object):
    def __init__(
            self,
            factor_cache: FactorCache = None,
            memoized_suitability_scores: Dict[Tuple[str, str], float]=None):
        if factor_cache is None:
            factor_cache = FactorCache()
        self._factor_cache = factor_cache
        if memoized_suitability_scores is None:
            memoized_suitability_scores = {}
        self._memoized_suitability_scores = memoized_suitability_scores

    def calculate_suitability_score(
            self, driver_name: str, street_address: str) -> float:
        key = (driver_name, street_address)

        if key not in self._memoized_suitability_scores:
            driver_factors = \
                self._factor_cache.get_prime_factors_by_name(driver_name)
            base_suitability_score = calculate_base_suitability_score(
                driver_name, street_address)

            street_factors = \
                self._factor_cache.get_prime_factors_by_name(street_address)
            common_factors = driver_factors.intersection(street_factors)

            if len(common_factors) > 0:
                self._memoized_suitability_scores[key] \
                    = base_suitability_score * 1.5
            else:
                self._memoized_suitability_scores[key] = base_suitability_score

        return self._memoized_suitability_scores[key]
