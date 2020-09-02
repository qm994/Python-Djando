from django.test import TestCase 
from app.calc import add, subtract

class CalcTests(TestCase):
    # all the test functions must start with `test_`
    def test_add_numbers(self):
        "Test the two numbers are added together function"
        self.assertEqual(add(3,8), 11)

    def test_subtract_numbers(self):
        """Test values are subtracted and returned"""
        self.assertEqual(subtract(5, 11), 6)
        