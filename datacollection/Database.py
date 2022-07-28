import unittest
from .models import DataQuelle

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        pass
    def test_something(self):
        quelle = DataQuelle.objects.get(protokol='mqtt')


if __name__ == '__main__':
    unittest.main()
