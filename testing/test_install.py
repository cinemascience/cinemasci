import unittest
import filecmp
import cinemasci
import os.path
import shutil

class TestInstall(unittest.TestCase):
    data_dir    = "testing/data"
    gold_dir    = "testing/gold/cdb"
    scratch_dir = "testing/scratch/cdb"

    def __init__(self, *args, **kwargs):
        super(TestInstall, self).__init__(*args, **kwargs)

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def test_install(self):
        source_cdb = os.path.join(TestInstall.data_dir, "phi-theta.cdb")
        shutil.copytree(source_cdb, ".")
        names = shutil.listdir(".")
        for name in names:
            print(name)
