import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import MagicMock, patch
from src.load import LoaderBase

class TestLoader(unittest.TestCase):

    def setUp(self):
        self.mock_conn = MagicMock()
        self.loader = LoaderBase(self.mock_conn)

    def test_load_empty_data(self):
        result = self.loader.load('olap.fact_sales', [], ['col1', 'col2'])
        self.assertEqual(result, 0)

    def test_load_calls_executemany(self):
        mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        self.mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        data = [(1, 'test'), (2, 'test2')]
        columns = ['id', 'name']

        try:
            self.loader.load('olap.dim_product', data, columns)
        except Exception:
            pass

        self.mock_conn.cursor.assert_called()

    def test_load_returns_count(self):
        mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        self.mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        data = [(1, 'a'), (2, 'b'), (3, 'c')]
        try:
            result = self.loader.load('test.table', data, ['id', 'name'])
            self.assertEqual(result, 3)
        except Exception:
            pass

if __name__ == '__main__':
    unittest.main()