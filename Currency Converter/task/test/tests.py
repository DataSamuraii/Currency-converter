import unittest
from ..cconverter.cconverter import CurrencyConverter


class TestCurrencyConverter(unittest.TestCase):
    def setUp(self):
        self.converter = CurrencyConverter()

    def test_get_json(self):
        result = self.converter.get_json('USD')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_get_exchange_rate(self):
        self.converter.currency_dict = {'USD': {}}
        result = self.converter.get_exchange_rate('USD', 'eur')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_calculate_changed_amount(self):
        result = self.converter.calculate_changed_amount(100, 1.2)
        self.assertEqual(result, 120.0)

    def test_get_currency(self):
        # Assuming a method to set the user input, or you can use mocking
        result = self.converter.get_currency('Please enter the base currency: ', currency_type='base')
        self.assertIsInstance(result, list)
        self.assertIn('usd', result)

    def test_get_amount(self):
        # Assuming a method to set the user input, or you can use mocking
        result = self.converter.get_amount('Please enter the amount: ', min_=0)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
