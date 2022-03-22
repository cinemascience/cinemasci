import unittest
import filecmp
import cinemasci.install
import os.path
import shutil

class TestInstall(unittest.TestCase):
    data_dir    = "testing/data/phi-theta.cdb"
    gold_dir    = "testing/gold/cdb"
    install_dir = "testing/scratch/install"
    cdb_dir     = "testing/scratch/install/phi-theta.cdb"
    viewer_dir  = "cinemasci/viewers"

    def __init__(self, *args, **kwargs):
        super(TestInstall, self).__init__(*args, **kwargs)

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def test_install(self):
        print("null test")
        # shutil.copytree(TestInstall.data_dir, TestInstall.cdb_dir)
        # cinemasci.install.explorer(TestInstall.viewer_dir, TestInstall.install_dir, "cinema_explorer.html", "phi-theta.cdb") 
