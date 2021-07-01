from AMT import create_app
import unittest

class TestFactory(unittest.TestCase):

    def test_config(self):
        assert not create_app().testing
        assert create_app({'TESTING': True}).testing
    