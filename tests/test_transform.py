import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from src.transform import TransformerBase

class TestTransformer(unittest.TestCase):

    def setUp(self):
        self.transformer = TransformerBase()

    def test_clean_string_normal(self):
        self.assertEqual(self.transformer.clean_string('  hola  '), 'hola')

    def test_clean_string_none(self):
        self.assertIsNone(self.transformer.clean_string(None))

    def test_clean_numeric_normal(self):
        self.assertEqual(self.transformer.clean_numeric('3.14'), 3.14)

    def test_clean_numeric_none(self):
        self.assertEqual(self.transformer.clean_numeric(None), 0.0)

    def test_clean_numeric_invalid(self):
        self.assertEqual(self.transformer.clean_numeric('abc'), 0.0)

    def test_clean_date_none(self):
        self.assertIsNone(self.transformer.clean_date(None))

if __name__ == '__main__':
    unittest.main()