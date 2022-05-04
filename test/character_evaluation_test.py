from character_evaluation import is_consonant, is_vowel
from unittest import TestCase


class TestCharacterEvaluation(TestCase):
    def test_is_consonant_positive(self):
        self.assertTrue(is_consonant('r'))

    def test_is_consonant_negative(self):
        self.assertFalse(is_consonant('e'))

    def test_is_vowel_positive(self):
        self.assertTrue(is_vowel('e'))

    def test_is_vowel_negative(self):
        self.assertFalse(is_vowel('r'))
