import unittest
import filecmp
import cinemasci
import os.path
import shutil

class TestCDB(unittest.TestCase):
    gold_dir    = "testing/gold/cdb"
    scratch_dir = "testing/scratch/cdb"

    def __init__(self, *args, **kwargs):
        super(TestCDB, self).__init__(*args, **kwargs)

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def test_db_create_options(self):
        """Test creating a database when the directory exists
        """
        cdb_path = os.path.join(TestCDB.scratch_dir, "test_create_directory") 
        cdb = cinemasci.new("cdb", {"path": cdb_path})
        self.assertTrue(cdb.initialize())
        self.assertFalse(cdb.initialize())
        self.assertTrue(cdb.initialize(dirExistCheck=False))

    def test_unique_values(self):
        """Load a database from disk and check unique values for a column 
        """

        # testing a single extract database
        cdb_path = "testing/data/sphere.cdb"
        cdb = cinemasci.new("cdb", {"path": cdb_path})
        self.assertTrue(cdb.read_data_from_file())
        cdb.set_extract_parameter_names(["FILE"])

        # testing queries
        self.assertTrue(cdb.parameter_exists("theta"))
        self.assertFalse(cdb.parameter_exists("nothing"))
        self.assertTrue(cdb.extract_parameter_exists("FILE"))
        self.assertFalse(cdb.extract_parameter_exists("FILE_NONE"))

        # test return values 
        values = cdb.getParameterValues("phi")
        self.assertTrue(values, [0])
        values = cdb.getParameterValues("theta")
        self.assertTrue(values, [-180.0, -162.0, -144.0, -126.0, -108.0, -90.0, -72.0, -54.0, -36.0, -18.0, 0.0, 18.0, 36.0, 54.0, 72.0, 90.0, 108.0, 126.0, 144.0, 162.0])

    def test_load_cdb(self):
        """Load a database from disk and check it
        """

        # test failing to load a cdb that doesn't exist
        cdb_path = "testing/data/not_there.cdb"
        cdb = cinemasci.new("cdb", {"path": cdb_path})
        self.assertFalse(cdb.read_data_from_file())

        # testing a single extract database
        cdb_path = "testing/data/sphere.cdb"
        cdb = cinemasci.new("cdb", {"path": cdb_path})
        self.assertTrue(cdb.read_data_from_file())
        cdb.set_extract_parameter_names(["FILE"])

        # testing queries
        self.assertTrue(cdb.parameter_exists("theta"))
        self.assertFalse(cdb.parameter_exists("nothing"))
        self.assertTrue(cdb.extract_parameter_exists("FILE"))
        self.assertFalse(cdb.extract_parameter_exists("FILE_NONE"))

        # test the same query with parameters in different order
        extract = cdb.get_extracts({"theta": "0", "phi": "36"})
        self.assertEqual(extract, ["testing/data/sphere.cdb/image/36/0.png"])
        extract = cdb.get_extracts({"phi": "36", "theta": "0"})
        self.assertEqual(extract, ["testing/data/sphere.cdb/image/36/0.png"])

        # test a negative query (doesn't exist)
        extract = cdb.get_extracts({"phi": "96", "theta": "0"})
        self.assertEqual(extract, [])

    def test_null_nan_values(self):
        """Load a database and test a database with NULL and NaN values
        """
        cdb_path = "testing/data/test_values.cdb"
        cdb = cinemasci.new("cdb", {"path": cdb_path})
        self.assertTrue(cdb.read_data_from_file())

        cdb.set_extract_parameter_names(["path"])

        # testing queries
        self.assertTrue(cdb.parameter_exists("time"))
        self.assertTrue(cdb.parameter_exists("phi"))
        self.assertTrue(cdb.parameter_exists("theta"))
        self.assertFalse(cdb.parameter_exists("nothing"))
        self.assertTrue(cdb.extract_parameter_exists("path"))
        self.assertFalse(cdb.extract_parameter_exists("FILE"))

        # test the same query with parameters in different order
        extract = cdb.get_extracts({"time": "2.0", "phi": "1.0", "theta": "1.0"})
        self.assertEqual(extract, ["testing/data/test_values.cdb/0002/0000"])
        extract = cdb.get_extracts({"time": "", "phi": "1.0", "theta": "1.0"})
        self.assertEqual(extract, ["testing/data/test_values.cdb/0000/0000"])
        extract = cdb.get_extracts({"time": "1.0", "phi": "NaN", "theta": "1.0"})
        self.assertEqual(extract, ["testing/data/test_values.cdb/0001/0000"])

    def test_multiple_artifacts(self):
        """Load and test a database with multiple artifacts per parameter list
        """

        # testing a single extract database
        cdb_path = "testing/data/multiple_artifacts.cdb"
        cdb = cinemasci.new("cdb", {"path": cdb_path})
        self.assertTrue(cdb.read_data_from_file())
        cdb.set_extract_parameter_names(["FILE"])
        cdb.set_extract_parameter_names(["FILE2"])

        # testing queries
        self.assertTrue(cdb.parameter_exists("theta"))
        self.assertFalse(cdb.parameter_exists("nothing"))
        self.assertTrue(cdb.extract_parameter_exists("FILE"))
        self.assertFalse(cdb.extract_parameter_exists("FILE_NONE"))

        # test the same query with parameters in different order
        extract = cdb.get_extracts({"theta": "0", "phi": "36"})
        self.assertEqual(extract, ["testing/data/multiple_artifacts.cdb/image/36/0.png", 
                                        "testing/data/multiple_artifacts.cdb/image_02/36/0.png"])
        extract = cdb.get_extracts({"phi": "36", "theta": "0"})
        self.assertEqual(extract, ["testing/data/multiple_artifacts.cdb/image/36/0.png", 
                                        "testing/data/multiple_artifacts.cdb/image_02/36/0.png"])

        # test a negative query (doesn't exist)
        extract = cdb.get_extracts({"phi": "96", "theta": "0"})
        self.assertEqual(extract, [])

    def test_write_api(self):
        """Create a database from scratch, and test its output against a known result
        """

        dbname = "test_write_test.cdb"
        cdb_path = os.path.join(TestCDB.scratch_dir, dbname) 
        cdb = cinemasci.new("cdb", {"path": cdb_path})
        cdb.initialize()

        # insert entries in an order that tests the cdb's ability to order columns 
        # as described in the spec
        id = cdb.add_entry({'FILE02': '0002.png', 'time': '1.0', 'phi': '10.0', 'theta': '0.0'})
        id = cdb.add_entry({'time': '0.0', 'phi': '0.0', 'theta': '0.0', 'FILE': '0000.png'})
        id = cdb.add_entry({'time': '1.0', 'phi': '10.0', 'theta': '0.0', 'FILE01': '0001.png'})
        id = cdb.add_entry({'time': '1.0', 'FILE': '0003.png'})

        # write out the cdb
        cdb.finalize()

        # move the output to a specific name
        target_name = "test_write_api.cdb"
        target_path = os.path.join(TestCDB.scratch_dir, target_name)
        shutil.copytree(cdb_path, target_path)
        # test the result
        self.assertTrue(filecmp.cmp(os.path.join(TestCDB.gold_dir, target_name, cdb.get_data_filename()), 
                os.path.join(TestCDB.scratch_dir, target_name, cdb.get_data_filename())), "data.csv files are not the same")

        # delete and compare results to gold
        cdb.delete_entry(id)
        cdb.finalize()

        target_name = "test_delete_api.cdb"
        target_path = os.path.join(TestCDB.scratch_dir, target_name)
        shutil.copytree(cdb_path, target_path)
        # test the result
        self.assertTrue(filecmp.cmp(os.path.join(TestCDB.gold_dir, target_name, cdb.get_data_filename()), 
                os.path.join(TestCDB.scratch_dir, target_name, cdb.get_data_filename())), "data.csv files are not the same")
