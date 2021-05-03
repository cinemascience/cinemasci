import unittest
import filecmp
import cinemasci
import cinemasci.cis
import cinemasci.cis.view
import os.path
import shutil

class TestCISCDB(unittest.TestCase):
    gold_dir    = "testing/gold/cdb"
    scratch_dir = "testing/scratch/cdb"

    def __init__(self, *args, **kwargs):
        super(TestCISCDB, self).__init__(*args, **kwargs)

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def test_load_cdb(self):
        """Load a database from disk and check it
        """

        # testing a single extract database
        cdb_path = "testing/data/cis.cdb"
        cdb = cinemasci.new("cdb", {"path": cdb_path})
        self.assertTrue(cdb.read_data_from_file())
        cdb.set_extract_parameter_names(["FILE"])

        # testing queries
        self.assertTrue(cdb.parameter_exists("time"))
        self.assertTrue(cdb.parameter_exists("CISVersion"))
        self.assertFalse(cdb.parameter_exists("nothing"))
        self.assertTrue(cdb.extract_parameter_exists("FILE"))
        self.assertFalse(cdb.extract_parameter_exists("FILE_NONE"))

        # test the same query with parameters in different order
        images = cdb.get_cis_image_names()
        # print("images: {}".format(images))
        for i in images:
            layers = cdb.get_cis_image_layers(i) 
            # print("layers: {}".format(layers))
            for l in layers: 
                channels = cdb.get_cis_layer_channels(i, l) 
                # print("channels: {}".format(channels))
                for c in channels:
                    # print("{}:{}:{}".format(i, l, c))
                    extract = cdb.get_extracts(
                            {
                             "CISImage"     : i,
                             "CISLayer"     : l, 
                             "CISChannel"   : c 
                            })
                    # print(extract)
                    self.assertEqual(extract, ["testing/data/cis.cdb/image/{}/layer/{}/channel/{}/data.npz".format(i, l, c)])


        

    def test_create_cis_object(self):
        cdb_path = "testing/data/cis.cdb"
        cdb = cinemasci.new("cdb", {"path": cdb_path})

        self.assertTrue(cdb.read_data_from_file())
        cdb.set_extract_parameter_names(["FILE"])

        cview = cinemasci.cis.view.view(cdb)
        cview.set_image("i000")
        cview.set_layers(["l000", "l001"])
        cview.set_channels(["depth", "temperature"])
        extracts = cview.get_extracts({"time": "0.0"})
        for e in extracts:
            print(e)

        results = cview.get_image_parameters()
        print(results)

        results = cview.get_layer_parameters("l000")
        print(results)

        results = cview.get_channel_parameters("l000", "temperature")
        print(results)


