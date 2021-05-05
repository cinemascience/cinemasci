import unittest

import numpy as np

import cinemasci
import cinemasci.cis


class TestRenderer():

    def __init__(self):
        return

    # Paste buffer 'src' to buffer 'dest' at the 'offset' assuming dest is
    # large enough.
    @staticmethod
    def paste(dest, src, offset):
        ends = offset + src.shape
        # TODO: check on ends[] such that it actually fits. Does numpy
        #  automatically do this?
        dest[offset[0]:ends[0], offset[1]:ends[1], :] = src
        return dest

    # Color a scalar value buffer 'scalars' by the 'colormap'
    @staticmethod
    def color(scalars, colormap):
        # TODO: this is an NOP, replace it with the real stuff
        image = np.zeros((scalars.shape[0], scalars.shape[1], 3))
        image[:, :, 0] = scalars
        return image

    @staticmethod
    def blend(dest, src, mask):
        dest[mask] = src[mask]

    @staticmethod
    def depth_composite(dest_color, dest_z, src_color, src_z):
        mask = np.nan_to_num(dest_z, nan=np.inf) < \
               np.nan_to_num(src_z, nan=np.inf)
        TestRenderer.blend(dest_color, src_color, mask)
        TestRenderer.blend(dest_z, src_z, mask)

    #
    # an example of how to iterate over the datastructure
    #
    def render(self, iview):

        # FXIME: this assumes RGB rather than RGBA color
        canvas = np.zeros((iview.dims[0], iview.dims[1], 3), float)
        depth = np.ones((iview.dims[0], iview.dims[1])) * np.inf

        # TODO: how to make use of 'origin'?
        layers = iview.get_layer_data()
        for name, layer in layers.items():
            # TODO: where is the actual predefined colormaps aka. cis.colormaps?
            data = layer.channel.data
            colored = TestRenderer.color(data, layer.channel.colormap)
            rectangle = [
                slice(layer.offset[0], layer.offset[0] + data.shape[0]),
                slice(layer.offset[1], layer.offset[1] + data.shape[1])]
            if iview.use_depth:
                TestRenderer.depth_composite(canvas[tuple(rectangle)],
                                             depth[tuple(rectangle)],
                                             colored, layer.depth.data)
            else:
                canvas = TestRenderer.paste(canvas, colored, layer.offset)
                # else:
                # print("printing image")
                # print("  dims       : {}".format(iview.dims))
                # print("  origin     : {}".format(iview.origin))
                # print("  use_depth  : {}".format(iview.use_depth))
                # print("  use_shadow : {}".format(iview.use_shadow))
                # print()
                #
                # #
                # # layer data is a dictionary of layer objects
                # #
                # # 1. layers are composited in iterator order
                # # 2. each layer has a single active layer, and optional
                # #    'depth' and 'shadow' layers that can be used
                # #
                # print("  layers")
                # data = iview.get_layer_data()
                # for l in data:
                #     print("    name:    {}".format(data[l].name))
                # print("    offset:  {}".format(data[l].offset))
                # print("    dims:    {}".format(data[l].dims))
                # print("    channel:")
                # print("      name:     {}".format(data[l].channel.name))
                # print("      colormap: {}".format(data[l].channel.colormap))
                # print("      data:     {}".format(data[l].channel.data))
                #
                # # depth flag indicates whether or not to use the depth info
                # if iview.use_depth:
                #     print("    depth:")
                # print("      name:  {}".format(data[l].depth.name))
                # print("             {}".format(data[l].depth.data))
                # else:
                # print("NOT using DEPTH information")
                #
                # # shadow flag indicates whether or not to use the shadow info
                # if iview.use_shadow:
                #     print("    shadow:")
                # print("      name:  {}".format(data[l].shadow.name))
                # print("             {}".format(data[l].shadow.data))
                # else:
                # print("NOT using SHADOW information")

        return None


class TestCIS(unittest.TestCase):
    gold_dir = "testing/gold/cdb"
    scratch_dir = "testing/scratch/cdb"
    cdb_path = "testing/data/cis.cdb"

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
                            "CISImage": i,
                            "CISLayer": l,
                            "CISChannel": c
                        })
                    # print(extract)
                    self.assertEqual(extract, [
                        "testing/data/cis.cdb/image/{}/layer/{}/channel/{}/data.npz".format(
                            i, l, c)])

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
        self.assertEqual(results,
                         {
                             'dims': [1024, 768],
                             'origin': 'UL'
                         }
                         )

        results = cview.get_layer_parameters("i000", "l000")
        self.assertEqual(results, {'dims': [100, 200], 'offset': [0, 10]})

        results = cview.get_channel_parameters("i000", "l000", "temperature")
        self.assertEqual(results,
                         {
                             'variable': {
                                 'name': 'temperature',
                                 'range': ['10.0', '100.0']
                             },
                             'colormap': {
                                 'source': 'matplotlib',
                                 'name': 'gray'
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
        self.assertEqual(cview.channels,
                         {
                             "l000": ['CISDepth', 'CISShadow', 'pressure',
                                      'procID', 'temperature'],
                             "l001": ['CISDepth', 'CISShadow', 'pressure',
                                      'procID', 'temperature'],
                             "l002": ['CISDepth', 'CISShadow', 'pressure',
                                      'procID', 'temperature']
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

        # test render
        renderer = TestRenderer()
        image = renderer.render(iview)

    #
    # an example of loading a cinema dataset that includes CIS data
    # loading the CIS data, and then passing to a renderer
    #
    def test_render(self):
        cdb = cinemasci.new("cdb", {"path": TestCIS.cdb_path})

        self.assertTrue(cdb.read_data_from_file())
        cdb.set_extract_parameter_names(["FILE"])

        cview = cinemasci.cis.cdbview.cdbview(cdb)
        iview = cinemasci.cis.imageview.imageview(cview)

        # set the imageview state
        # activate/deactivate depth and shadow
        iview.use_depth = True
        iview.use_shadow = False
        # activate layers
        iview.activate_layer("l000")
        iview.activate_layer("l001")
        iview.activate_layer("l002")
        # activate channels (one per layer)
        iview.activate_channel("l000", "temperature")
        iview.activate_channel("l001", "pressure")
        iview.activate_channel("l002", "procID")

        # load data into the image view 
        # set the image
        iview.image = "i000"
        # update, which loads data per the state
        iview.update()

        renderer = TestRenderer()
        image = renderer.render(iview)
