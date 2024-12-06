#!/usr/bin/env python
import unittest
import app

class TestHello(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_hello(self):
        my_html = f"<body style='background-color: #6bc930;'><h1 style='color:  #0a0a0a;'>Green Version: V2</h1>"
        rv = self.app.get('/')
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data.decode('utf-8'), my_html)

    def test_hello_name(self):
        name = 'Shubham'
        my_html = f"<body style='background-color: #6bc930;'><h1 style='color:  #0a0a0a;'>Hello {name} you are accessing the Green Version of the app: V2</h1>"
        rv = self.app.get(f'/{name}')
        self.assertEqual(rv.status, '200 OK')
        self.assertIn(bytearray(f"{name}", 'utf-8'), rv.data)

if __name__ == '__main__':
    import xmlrunner
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)
    unittest.main()
    