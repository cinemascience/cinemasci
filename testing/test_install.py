import unittest
import filecmp
import cinemasci.install
import os.path
import shutil

class TestInstall(unittest.TestCase):
    viewers = ["explorer", "view", "simple"]
    src_basepath = "testing/data"
    src_dbs = ["sphere.cdb", "sedov1.cdb", "sedov2.cdb"]
    dbs = {
        "explorer": 
        [ 
                {
                    "name": "sphere",
                    "directory": "sphere.cdb"
                },
                {
                    "name": "sedov",
                    "directory": "sedov1.cdb"
                }
        ],
        "view": 
        [
            { 
                "database_name": "sphere",
                "datasets":
                [
                    {
                        "name": "sphere",
                        "location": "sphere.cdb"
                    }
                ]
            },
            { 
                "database_name": "sedov",
                "datasets":
                [
                    {
                        "name": "sedov1",
                        "location": "sedov1.cdb"
                    },
                    {
                        "name": "sedov2",
                        "location": "sedov2.cdb"
                    }
                ]
            }
        ],
        "simple": [ "sedov1.cdb" ]
    }

    def __init__(self, *args, **kwargs):
        super(TestInstall, self).__init__(*args, **kwargs)

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def __install(self, itype):
        for v in self.viewers:
            print("Viewer: {}".format(v))
            # basics
            res_basepath = "./testing/scratch/install/{}/{}".format(itype, v)
            print(res_basepath)

            # expand path
            abs_basepath = os.path.abspath(os.path.expanduser(res_basepath))

            # copy data to testing area
            for db in self.src_dbs:
                shutil.copytree( "{}/{}".format(self.src_basepath, db), "{}/{}".format(res_basepath, db) ) 

            # viewer install
            destination = abs_basepath
            installer = cinemasci.install.install()
            installer.install_viewer( destination, v, self.dbs[v], itype )

    def test_local_install(self):
        self.__install("local")

    def test_remote_install(self):
        self.__install("remote")
