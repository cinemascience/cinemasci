import unittest
import filecmp
import cinemas
import os.path

class TestCDB(unittest.TestCase):
    gold_dir    = "testing/gold/cdb"
    scratch_dir = "testing/scratch/cdb"

    def __init__(self, *args, **kwargs):
        super(TestCDB, self).__init__(*args, **kwargs)

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def test_load_cdb(self):
        """Load a database from disk and check it
        """

        # test failing to load a cdb that doesn't exist
        cdb_path = "testing/data/not_there.cdb"
        cdb = cinemas.cdb.cdb(cdb_path)
        self.assertFalse(cdb.read_data_from_file())

        # testing a single extract database
        cdb_path = "testing/data/sphere.cdb"
        cdb = cinemas.cdb.cdb(cdb_path)
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
        cdb = cinemas.cdb.cdb(cdb_path)
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
        cdb = cinemas.cdb.cdb(cdb_path)
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
        self.assertEqual(extract, ["testing/data/multiple_artifacts.cdb/image/36/0.png", "testing/data/multiple_artifacts.cdb/image_02/36/0.png"])
        extract = cdb.get_extracts({"phi": "36", "theta": "0"})
        self.assertEqual(extract, ["testing/data/multiple_artifacts.cdb/image/36/0.png", "testing/data/multiple_artifacts.cdb/image_02/36/0.png"])

        # test a negative query (doesn't exist)
        extract = cdb.get_extracts({"phi": "96", "theta": "0"})
        self.assertEqual(extract, [])

    def test_write_api(self):
        """Create a database from scratch, and test its output against a know result
        """

        dbname = "test_write.cdb"
        datafile = "data.csv"
        cdb_path = os.path.join(TestCDB.scratch_dir, dbname) 
        cdb = cinemas.cdb.cdb(cdb_path)
        cdb.initialize()

        id = cdb.add_entry({'time': '0.0', 'phi': '0.0', 'theta': '0.0', 'FILE': '0000.png'})
        id = cdb.add_entry({'time': '1.0', 'phi': '10.0', 'theta': '0.0', 'FILE01': '0001.png'})
        id = cdb.add_entry({'time': '1.0', 'FILE': '0002.png'})

        cdb.finalize()
        self.assertTrue(filecmp.cmp(os.path.join(TestCDB.gold_dir, dbname, datafile), 
                os.path.join(cdb_path, datafile)), "data.csv files are not the same")

        # delete and compare results to gold
        dbname = "test_delete.cdb"
        cdb.delete_entry(id)
        cdb.finalize()
        self.assertTrue(filecmp.cmp(os.path.join(TestCDB.gold_dir, dbname, datafile), 
                os.path.join(cdb_path, datafile)), "data.csv files are not the same")
