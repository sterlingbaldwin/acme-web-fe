import unittest
import requests
import os


class Testresponses(unittest.TestCase):

    def test_get_all(self):
        payload = {'status': 'all'}
        r = requests.get('http://127.0.0.1:8000/poller/', params=payload)
        self.assertEqual(str(r), '<Response [200]>')

    def test_get_new(self):
        payload = {'status': 'new'}
        r = requests.get('http://127.0.0.1:8000/poller/', params=payload)
        self.assertEqual(str(r), '<Response [200]>')

    def test_get_in_progress(self):
        payload = {'status': 'in_progress'}
        r = requests.get('http://127.0.0.1:8000/poller/', params=payload)
        self.assertEqual(str(r), '<Response [200]>')

    def test_get_complete(self):
        payload = {'status': 'complete'}
        r = requests.get('http://127.0.0.1:8000/poller/', params=payload)
        self.assertEqual(str(r), '<Response [200]>')

    def test_get_failed(self):
        payload = {'status': 'failed'}
        r = requests.get('http://127.0.0.1:8000/poller/', params=payload)
        self.assertEqual(str(r), '<Response [200]>')


os.system('clear')
suite = unittest.TestLoader().loadTestsFromTestCase(Testresponses)
unittest.TextTestRunner(verbosity=2).run(suite)
