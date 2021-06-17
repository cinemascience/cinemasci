import unittest
import numpy

import cinemasci
import cinemasci.cis
from cinemasci.cis.renderer import Renderer

SAVE_IMAGE_HACK = False

class TestCIS(unittest.TestCase):
    gold_dir            = "testing/gold/cdb"
    scratch_dir         = "testing/scratch/cdb"
    cdb_path            = "testing/gold/cis/random/cis.cdb"
    constant_cdb_path   = "testing/gold/cis/constant/cis.cdb"
    linear_cdb_path     = "testing/gold/cis/linear/cis.cdb"
    random_cdb_path     = "testing/gold/cis/random/cis.cdb"
    ascent_cdb_path     = "testing/data/pantheon_ascent-clover.cdb"
    paraview_cdb_path   = "testing/data/paraview_extracts.cdb"
    ttk_cdb_path        = "testing/data/ttk_extracts_001.cdb"

    def __init__(self, *args, **kwargs):
        super(TestCIS, self).__init__(*args, **kwargs)

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def test_load_cdb(self):
        """Load a database from disk and check it
        """

        # testing a single extract database
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
                        "testing/gold/cis/random/cis.cdb/image/{}/layer/{}/channel/{}/data.npz".format(
                            i, l, c)])

    def test_create_cis_view(self):
        cdb = cinemasci.new("cdb", {"path": TestCIS.cdb_path})

        self.assertTrue(cdb.read_data_from_file())
        cdb.set_extract_parameter_names(["FILE"])

        cview = cinemasci.cis.cdbview.cdbview(cdb)
        extracts = cview.get_channel_extracts("i000", "l000")
        expected = [
            "testing/gold/cis/random/cis.cdb/image/i000/layer/l000/channel/CISDepth/data.npz",
            "testing/gold/cis/random/cis.cdb/image/i000/layer/l000/channel/CISShadow/data.npz",
            "testing/gold/cis/random/cis.cdb/image/i000/layer/l000/channel/pressure/data.npz",
            "testing/gold/cis/random/cis.cdb/image/i000/layer/l000/channel/procID/data.npz",
            "testing/gold/cis/random/cis.cdb/image/i000/layer/l000/channel/temperature/data.npz"
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
                                 'name' : 'temperature',
                                 'type' : 'float',
                                 'min'  : '10.0',
                                 'max'  : '100.0',
                             },
                             'colormap': {
                                 'type': 'url',
                                 'url' : 'colormaps/cooltowarm.json'
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

        # check some float values
        layers = iview.get_layer_data()
        self.assertEqual(0.5032877357241973, numpy.nanmean(layers['l000'].channel.data))

        # check a colormap
        layers = iview.get_layer_data()
        l = 'l000'
        self.assertEqual(   'rgb', layers[l].channel.colormap["colorspace"])
        self.assertEqual(   layers[l].channel.colormap["points"][0], 
                            {'x': 0.0, 'r': 0.23137254902, 'g': 0.298039215686, 'b': 0.752941176471, 'a': 1.0} ) 
        self.assertEqual(   layers[l].channel.colormap["points"][1], 
                            {'x': 0.5, 'r': 0.865, 'g': 0.865, 'b': 0.865, 'a': 1.0} )
        self.assertEqual(   layers[l].channel.colormap["points"][2], 
                            {'x': 1, 'r': 0.705882352941, 'g': 0.0156862745098, 'b': 0.149019607843, 'a': 1.0} )

        # check the updated iview object
        self.assertEqual(iview.dims, [1024, 768])
        self.assertEqual(iview.origin, "UL")

        # test render
        (image, depth) = Renderer.render(iview)
        import matplotlib.pyplot as plt
        import skimage.util
        plt.imshow(skimage.util.img_as_ubyte(image))
        plt.show()

    def dont_test_imageview(self):
        cdb = cinemasci.new("cdb", {"path": TestCIS.ttk_cdb_path})

        self.assertTrue(cdb.read_data_from_file())
        cdb.set_extract_parameter_names(["FILE"])

        # create cis view and an image view
        cview = cinemasci.cis.cdbview.cdbview(cdb)
        iview = cinemasci.cis.imageview.imageview(cview)

        # set the imageview state
        iview.image = "i000"
        iview.use_depth = True
        iview.use_shadow = True
        iview.activate_layer("l000")
        iview.activate_channel("l000", "Elevation")
        iview.activate_layer("l001")
        iview.activate_channel("l001", "Elevation")

        # load data into the image view 
        iview.update()

        for im in iview.get_active_layers():
            print("active layer: {}".format(im))
            data = iview.get_active_channel_data(im)

    #
    # an example of loading a cinema dataset that includes CIS data
    # loading the CIS data, and then passing to a renderer
    #
    def test_render(self):
        cdb = cinemasci.new("cdb", {"path": TestCIS.linear_cdb_path})

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
        
        self.assertEqual(cview.get_image({"time": "0.0"}), "i000")
        self.assertEqual(cview.get_image({"time": "1.0"}), "i001")
        self.assertEqual(cview.get_image({"time": "2.0"}), "i002")

        # load data into the image view 
        # set the image
        iview.image = "i000"
        # update, which loads data per the state
        iview.update()

        (image, depth) = Renderer.render(iview)

        import matplotlib.pyplot as plt
        import skimage.util
        plt.imshow(skimage.util.img_as_ubyte(image))
        plt.show()

        # change the background
        iview.background = [0.5, 0.5, 0.5]
        (image, depth) = Renderer.render(iview)
        plt.imshow(skimage.util.img_as_ubyte(image))
        if SAVE_IMAGE_HACK:
            plt.imsave("render.png", image)
        plt.show()

    #
    # test for loading paraview-generated data 
    #
    def test_render_paraview_data(self):
        cdb = cinemasci.new("cdb", {"path": TestCIS.paraview_cdb_path})

        self.assertTrue(cdb.read_data_from_file())
        cdb.set_extract_parameter_names(["FILE"])

        # create cis view and an image view
        cview = cinemasci.cis.cdbview.cdbview(cdb)
        iview = cinemasci.cis.imageview.imageview(cview)

        # set the imageview state
        iview.image = "i000"
        iview.use_depth = False
        iview.use_shadow = False
        iview.activate_layer("l000")
        iview.activate_channel("l000", "scalars")

        # load data into the image view 
        iview.update()

        # check some float values
        # layers = iview.get_layer_data()
        # self.assertEqual( 2.027437210083008, numpy.nanmean(layers['layer0'].channel.data))
        # self.assertNotEqual( 0.0, numpy.nanmean(layers['layer0'].channel.data))

        # render
        (image, depth) = Renderer.render(iview)

        # display the image
        import matplotlib.pyplot as plt
        import skimage.util
        plt.imshow(skimage.util.img_as_ubyte(image))
        plt.show()

        # change the background
        iview.background = [0.5, 0.5, 0.5]
        (image, depth) = Renderer.render(iview)
        plt.imshow(skimage.util.img_as_ubyte(image))
        if SAVE_IMAGE_HACK:
            plt.imsave("paraview.png", image)
        plt.show()

    #
    # an example of loading a cinema dataset that includes CIS data
    # loading the CIS data, and then passing to a renderer
    #
    def test_render_ascent_data(self):
        cdb = cinemasci.new("cdb", {"path": TestCIS.ascent_cdb_path})

        self.assertTrue(cdb.read_data_from_file())
        cdb.set_extract_parameter_names(["FILE"])

        # create cis view and an image view
        cview = cinemasci.cis.cdbview.cdbview(cdb)
        iview = cinemasci.cis.imageview.imageview(cview)

        # set the imageview state
        iview.image = "cycle_000100"
        iview.use_depth = False
        iview.use_shadow = False
        iview.activate_layer("layer0")
        iview.activate_channel("layer0", "energy")

        # load data into the image view 
        iview.update()

        # check some float values
        layers = iview.get_layer_data()
        self.assertEqual( 2.027437210083008, numpy.nanmean(layers['layer0'].channel.data))
        self.assertNotEqual( 0.0, numpy.nanmean(layers['layer0'].channel.data))

        # render
        (image, depth) = Renderer.render(iview)

        # display the image
        import matplotlib.pyplot as plt
        import skimage.util
        plt.imshow(skimage.util.img_as_ubyte(image))
        plt.show()

        # change the background
        iview.background = [0.5, 0.5, 0.5]
        (image, depth) = Renderer.render(iview)
        plt.imshow(skimage.util.img_as_ubyte(image))
        if SAVE_IMAGE_HACK:
            plt.imsave("ascent.png", image)
        plt.show()

    #
    # test for loading paraview-generated data 
    #
    def test_render_ttk_data(self):
        cdb = cinemasci.new("cdb", {"path": TestCIS.ttk_cdb_path})

        self.assertTrue(cdb.read_data_from_file())
        cdb.set_extract_parameter_names(["FILE"])

        # create cis view and an image view
        cview = cinemasci.cis.cdbview.cdbview(cdb)
        iview = cinemasci.cis.imageview.imageview(cview)

        # set the imageview state
        iview.image = "i000"
        iview.use_depth = True
        iview.use_shadow = False
        iview.activate_layer("l000")
        iview.activate_channel("l000", "Elevation")
        iview.activate_layer("l001")
        iview.activate_channel("l001", "Elevation")

        # load data into the image view 
        iview.update()

        # render
        (image, depth) = Renderer.render(iview)

        # display the image
        import matplotlib.pyplot as plt
        import skimage.util
        plt.imshow(skimage.util.img_as_ubyte(image))
        plt.show()

        # change the background
        iview.background = [0.5, 0.5, 0.5]
        (image, depth) = Renderer.render(iview)
        plt.imshow(skimage.util.img_as_ubyte(image))
        if SAVE_IMAGE_HACK:
            plt.imsave("ttk_composited.png", image)
        plt.show()

        # turn on shadows
        iview.use_shadow = True
        iview.update()
        (image, depth) = Renderer.render(iview)
        plt.imshow(skimage.util.img_as_ubyte(image))
        if SAVE_IMAGE_HACK:
            plt.imsave("ttk_composited_with_shadows.png", image)
        plt.show()

        # change the background
        iview.activate_layer("l000")
        iview.deactivate_layer("l001")
        iview.update()
        (image, depth) = Renderer.render(iview)
        plt.imshow(skimage.util.img_as_ubyte(image))
        if SAVE_IMAGE_HACK:
            plt.imsave("ttk_streamlines.png", image)
        plt.show()

        iview.activate_layer("l001")
        iview.deactivate_layer("l000")
        iview.update()
        (image, depth) = Renderer.render(iview)
        plt.imshow(skimage.util.img_as_ubyte(image))
        if SAVE_IMAGE_HACK:
            plt.imsave("ttk_stones.png", image)
        plt.show()
