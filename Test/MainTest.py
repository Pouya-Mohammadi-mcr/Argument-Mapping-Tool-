import unittest
import AMT

class MainTest(unittest.TestCase):

    def setUp(self):
        self.app = AMT.app.test_client()


    def test_home(self):
        r = self.app.get("/")
        self.assertEqual(200, r.status_code, "Status code was not 'OK'.")


if __name__ == '__main__':
    unittest.main()