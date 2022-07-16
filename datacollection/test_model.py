import unittest
from .models import DataQuelle


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_should_create_Dataquelle(self):
        dq = DataQuelle.objects.create(server = 'localhost:8083',protokol = 'mqtt',
                                       variable_address = '/test/sin',variable_name = 'strom')
        dq.save()
        self.assertEqual(str(dq),'mqtt')


if __name__ == '__main__':
    MyTestCase.test_should_create_Dataquelle()
    #unittest.main()
