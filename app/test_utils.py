import unittest
from utils import parse_address, identify_number, parse_streets, find_directions

class ParseTestCase(unittest.TestCase):
    """Tests for `utils.py`."""

    def test_is_string_true(self):
        """Does the function return a string?"""
        self.assertTrue(parse_address("ontario st"))

    def test_no_argument(self):
        """Does the function return nothing if you pass it nothing?"""
        self.assertFalse(parse_address(None))

    def test_uppercase(self):
        """Does the function return an uppercase string?"""
        self.assertEqual(parse_address('ontario st'), 'ONTARIO ST')
        self.assertEqual(parse_address('w 18th av'), 'W 18TH AV')
        self.assertEqual(parse_address('456 w 18th av'), '456 W 18TH AV')

    def test_number_identifier(self):
        """Does the function identify house numbers?"""
        self.assertEqual(identify_number(['456','ONTARIO','ST']),('456', ['ONTARIO','ST']))
        self.assertEqual(identify_number(['18TH', 'AV']),('', ['18TH','AV']))
        self.assertEqual(identify_number(['ONTARIO', 'ST']),('', ['ONTARIO','ST']))

    def test_remove_periods(self):
        """Does the function remove periods?"""
        self.assertEqual(parse_streets(['ST.','CLAIR','PLACE']), ['ST','CLAIR','PLACE'])

    def test_remove_apostrophes(self):
        """Does the function remove apostrophes?"""
        self.assertEqual(parse_streets(['ANGLER\'S','PLACE']), ['ANGLERS','PLACE'])

    def test_finding_directions(self):
        """Does the function identify multiple direction options?"""
        self.assertTrue(find_directions(['W','18TH','AV']))
        self.assertTrue(find_directions(['E','37TH','AV']))
        self.assertFalse(find_directions(['ONTARIO','ST']))
        self.assertFalse(find_directions(['EASTDALE','AV']))

if __name__ == '__main__':
    unittest.main()
