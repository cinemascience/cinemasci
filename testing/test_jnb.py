import unittest
import cinemasci

class TestPYNB(unittest.TestCase):

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def test_hello(self):
        viewer = cinemasci.pynb.CinemaViewer()
        viewer.setLayoutToHorizontal()
        viewer.setHeight(250)


if __name__ == '__main__':
    unittest.main()
