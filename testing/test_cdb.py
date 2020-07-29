import unittest
import cinesci

class TestCDB(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCDB, self).__init__(*args, **kwargs)

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def test_load_cdb(self):
        # test failing to load a cdb that doesn't exist
        cdb_path = "testing/data/not_there.cdb"
        cdb = cinesci.cdb.cdb(cdb_path)
        self.assertFalse(cdb.read_data_from_file())

        # testing a single extract database
        cdb_path = "testing/data/sphere.cdb"
        cdb = cinesci.cdb.cdb(cdb_path)
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
        cdb_path = "testing/data/test_values.cdb"
        cdb = cinesci.cdb.cdb(cdb_path)
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
        # testing a single extract database
        cdb_path = "testing/data/multiple_artifacts.cdb"
        cdb = cinesci.cdb.cdb(cdb_path)
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

    def test_write(self):
        cdb_path = "testing/scratch/new.cdb"
        cdb = cinesci.cdb.cdb(cdb_path)
        cdb.initialize()

        entry = {'time': '0.0', 'phi': '0.0', 'theta': '0.0', 'FILE': '0000.png'}
        cdb.add_entry(entry)
        entry = {'time': '1.0', 'phi': '10.0', 'theta': '0.0', 'FILE01': '0001.png'}
        cdb.add_entry(entry)
        entry = {'time': '1.0', 'FILE': '0002.png'}
        cdb.add_entry(entry)

        cdb.finalize()
