from suitability_score import \
    calculate_base_suitability_score_even_destination, \
    calculate_base_suitability_score_odd_destination, \
    calculate_base_suitability_score, SuitabilityScoreCalculator
from unittest import TestCase


class TestSuitabilityScore(TestCase):
    def test_calculate_base_suitability_score_even_destination_using_even_destination(
            self):
        self.assertEqual(
            4.5,
            calculate_base_suitability_score_even_destination(
                'Red Barclay',
                '12'))

    def test_calculate_base_suitability_score_even_destination_using_odd_destination(
            self):
        with self.assertRaises(AssertionError):
            calculate_base_suitability_score_even_destination(
                'Homer Simpson',
                '123')

    def test_calculate_base_suitability_score_odd_destination_using_even_destination(
            self):
        with self.assertRaises(AssertionError):
            calculate_base_suitability_score_odd_destination(
                'Red Simpson',
                '1234')

    def test_calculate_base_suitability_score_odd_destination_using_odd_destination(
            self):
        self.assertEqual(
            13.5,
            calculate_base_suitability_score_odd_destination(
                'Homer Barclay',
                '12345'))

    def test_calculate_base_suitability_score_using_even_destination(self):
        self.assertEqual(
            6,
            calculate_base_suitability_score(
                'Bo Darville',
                '123456'))

    def test_calculate_base_suitability_score_using_odd_destination(self):
        self.assertEqual(
            13.5,
            calculate_base_suitability_score(
                'Homer Darville',
                '1234567'))


class TestSuitabilityScoreCalculator(TestCase):
    def setUp(self):
        self._suitability_score_calculator = SuitabilityScoreCalculator()

    def test_calculate_suitability_score(self):
        self.assertEqual(
            4.5,
            self._suitability_score_calculator.calculate_suitability_score(
                'Cledus Snow',
                '4 Privet Drive'
            )
        )

