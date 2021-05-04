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
        images = cview.images
        # print("images: {}".format(images))
        for i in images:
            layers = cview.layers
            # print("layers: {}".format(layers))
            for l in layers: 
                channels = cview.channels[l]
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
        extracts = cview.get_channel_extracts("i000", "l000")
        expected = [ 
                        "testing/data/cis.cdb/image/i000/layer/l000/channel/CISDepth/data.npz",
                        "testing/data/cis.cdb/image/i000/layer/l000/channel/CISShadow/data.npz",
                        "testing/data/cis.cdb/image/i000/layer/l000/channel/pressure/data.npz",
                        "testing/data/cis.cdb/image/i000/layer/l000/channel/procID/data.npz",
                        "testing/data/cis.cdb/image/i000/layer/l000/channel/temperature/data.npz"
                  ]
        self.assertEqual(extracts, expected)

        results = cview.get_image_parameters()
        self.assertEqual(   results, 
                            {
                                'dims': [1024, 768],
                                'origin' : 'UL'
                            }
                        )

        results = cview.get_layer_parameters("i000", "l000")
        self.assertEqual(results, {'dims': [100, 200], 'offset': [0, 10]})

        results = cview.get_channel_parameters("i000", "l000", "temperature")
        self.assertEqual(   results, 
                            {
                                'variable': {
                                    'name' : 'temperature', 
                                    'range': ['10.0', '100.0']
                                },
                                'colormap' : {
                                    'source' : 'matplotlib',
                                    'name'   : 'gray'
                                }
                            }
                        )


    def test_create_image_views(self):
        cdb = cinemasci.new("cdb", {"path": TestCIS.cdb_path})

        self.assertTrue(cdb.read_data_from_file())
        cdb.set_extract_parameter_names(["FILE"])

        cview = cinemasci.cis.cdbview.cdbview(cdb)
        iview = cinemasci.cis.imageview.imageview(cview)

        # test the cisview 
        self.assertEqual(cview.images, ['i000', 'i001', 'i002'])
        self.assertNotEqual(cview.images, ['i000', 'i001', 'i003'])
        self.assertEqual(cview.layers, ['l000', 'l001', 'l002'])
        self.assertEqual(   cview.channels, 
                            {   
                                "l000" : ['CISDepth', 'CISShadow', 'pressure', 'procID', 'temperature'],
                                "l001" : ['CISDepth', 'CISShadow', 'pressure', 'procID', 'temperature'],
                                "l002" : ['CISDepth', 'CISShadow', 'pressure', 'procID', 'temperature']
                            }
                        )    
        self.assertEqual(True, cview.depth)
        self.assertEqual(True, cview.shadow)

        # set the state
        self.assertEqual(iview.use_depth, False)
        self.assertEqual(iview.use_shadow, False)
        iview.use_depth = True
        iview.use_shadow = False
        iview.activate_layer("l000")
        iview.activate_layer("l001")
        iview.activate_layer("l002")
        iview.activate_channel("l000", "temperature")
        iview.activate_channel("l001", "pressure")
        iview.activate_channel("l002", "procID")

        layers = []
        for l in iview.get_active_layers():
            layers.append(l)
        self.assertEqual(layers, ['l000', 'l001', 'l002'])

        self.assertEqual(iview.get_active_layers(), ['l000', 'l001', 'l002'])
        self.assertEqual(iview.get_active_channel("l000"), 'temperature')
        self.assertEqual(iview.get_active_channel("l001"), 'pressure')
        self.assertEqual(iview.get_active_channel("l002"), 'procID')

        # update
        iview.image = "i000"
        iview.update()

        # check the updated iview object
        self.assertEqual(iview.dims, [1024, 768])
        self.assertEqual(iview.origin, "UL")

        # iterate over the datastructure
        if True:
            print("printing image")
            print("  dims       :   {}".format(iview.dims))
            print("  origin     : {}".format(iview.origin))
            print("  use_depth  : {}".format(iview.use_depth))
            print("  use_shadow : {}".format(iview.use_shadow))
            print()
            data = iview.get_layer_data()
            print("  layers")
            for d in data:
                print("    name:    {}".format(data[d].name))
                print("    offset:  {}".format(data[d].offset))
                print("    dims:    {}".format(data[d].dims))
                print("    channel:")
                print("      name:     {}".format(data[d].channel.name))
                print("      colormap: {}".format(data[d].channel.colormap))
                print("      data:     {}".format(data[d].channel.data))
                if not data[d].depth is None:
                    print("    depth:   {}".format(data[d].depth.name))
                    print("             {}".format(data[d].depth.data))
                if not data[d].shadow is None:
                    print("    shadow:  {}".format(data[d].shadow.name))
                    print("             {}".format(data[d].shadow.data))

