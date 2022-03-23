import unittest
import filecmp
import cinemasci.install
import os.path
import shutil

class TestInstall(unittest.TestCase):
    gold_dir    = "testing/gold/cdb"
    scratch_dir = "testing/scratch/cdb"

    def __init__(self, *args, **kwargs):
        super(TestInstall, self).__init__(*args, **kwargs)

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def test_smoketest(self):
        cinemasci.install.smoketest()
