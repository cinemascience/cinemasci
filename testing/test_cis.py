import unittest
import filecmp
import cinemasci
import cinemasci.cis
import os.path
import shutil

class TestCIS(unittest.TestCase):
    gold_dir    = "testing/gold/cdb"
    scratch_dir = "testing/scratch/cdb"
    cdb_path    = "testing/data/cis.cdb"

    def __init__(self, *args, **kwargs):
        super(TestCIS, self).__init__(*args, **kwargs)

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def test_load_cdb(self):
        """Load a database from disk and check it
        """

        # testing a single extract database
        TestCIS.cdb_path = "testing/data/cis.cdb"
        cdb = cinemasci.new("cdb", {"path": TestCIS.cdb_path})
        self.assertTrue(cdb.read_data_from_file())
        cdb.set_extract_parameter_names(["FILE"])

        # testing queries
        self.assertTrue(cdb.parameter_exists("time"))
        self.assertTrue(cdb.parameter_exists("CISVersion"))
        self.assertFalse(cdb.parameter_exists("nothing"))
        self.assertTrue(cdb.extract_parameter_exists("FILE"))
        self.assertFalse(cdb.extract_parameter_exists("FILE_NONE"))

        # cis view
        cview = cinemasci.cis.cdbview.cdbview(cdb)

        # test the same query with parameters in different order
        images = cview.get_image_names()
        # print("images: {}".format(images))
        for i in images:
            layers = cview.get_image_layers(i) 
            # print("layers: {}".format(layers))
            for l in layers: 
                channels = cview.get_layer_channels(i, l) 
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


        

    def test_create_cis_view(self):
        cdb = cinemasci.new("cdb", {"path": TestCIS.cdb_path})

        self.assertTrue(cdb.read_data_from_file())
        cdb.set_extract_parameter_names(["FILE"])

        cview = cinemasci.cis.cdbview.cdbview(cdb)
        cview.set_image("i000")
        cview.set_layers(["l000", "l001"])
        cview.set_channels(["pressure", "temperature"])
        extracts = cview.get_extracts({"time": "0.0"})
        expected = [ "testing/data/cis.cdb/image/i000/layer/l000/channel/pressure/data.npz",
                    "testing/data/cis.cdb/image/i000/layer/l000/channel/temperature/data.npz",
                    "testing/data/cis.cdb/image/i000/layer/l001/channel/pressure/data.npz",
                    "testing/data/cis.cdb/image/i000/layer/l001/channel/temperature/data.npz"
                  ]
        self.assertEqual(extracts, expected)

        results = cview.get_image_parameters()
        self.assertEqual(results, {'dims': [1024, 768]})

        results = cview.get_layer_parameters("l000")
        self.assertEqual(results, {'dims': [100, 200], 'offset': [0, 10]})

        results = cview.get_channel_parameters("l000", "temperature")
        self.assertEqual(results, {'variable': 'temperature', 'range': ['10.0', '100.0']})



    def test_create_image_views(self):
        cdb = cinemasci.new("cdb", {"path": TestCIS.cdb_path})

        self.assertTrue(cdb.read_data_from_file())
        cdb.set_extract_parameter_names(["FILE"])

        cview = cinemasci.cis.cdbview.cdbview(cdb)
        iview = cinemasci.cis.imageview.imageview(cview)

        # test the same query with parameters in different order
        images = cview.get_image_names()
        self.assertEqual(images, ['i000', 'i001', 'i002'])

        layers = cview.get_layer_names()
        self.assertEqual(layers, ['l000', 'l001', 'l002'])

        channels = cview.get_channel_names()
        self.assertEqual(channels, ['CISDepth', 'CISLighting', 'pressure', 'procID', 'temperature'])

        depth = cview.get_depth()
        self.assertEqual(True, depth)

        lighting = cview.get_lighting()
        self.assertEqual(True, lighting)

        # set the state
        iview.depth = True
        iview.lighting = False
        iview.activate_layer("l000")
        iview.activate_layer("l001")
        iview.activate_channel("pressure")

        layers = []
        for l in iview.get_active_layers():
            layers.append(l)
        self.assertEqual(layers, ['l000', 'l001'])

        channels = []
        for c in iview.get_active_channels():
            channels.append(c)
        self.assertEqual(channels, ['CISDepth', 'pressure'])

        # update
        iview.update()

        # print("after update")
        # print(iview.dims)
        # for l in iview.data:
            # print(l.name)



