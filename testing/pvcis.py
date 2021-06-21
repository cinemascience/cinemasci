import unittest

import cinemasci
import cinemasci.cdb
import cinemasci.cis
import cinemasci.pynb
from cinemasci.cis.renderer import Renderer

class TestPVCIS(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestPVCIS, self).__init__(*args, **kwargs)

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def test_pvcis(self):
        # read cinema database
        cdb = cinemasci.cdb.cdb("testing/data/paraview_extracts.cdb")
        cdb.read_data_from_file()
        cdb.set_extract_parameter_names(["FILE"])

        # create the cis view and an image view
        cview = cinemasci.cis.cisview.cisview(cdb)
        iview = cinemasci.cis.imageview.imageview(cview)

        # set the image view state
        iview.image      = "i000"
        iview.use_depth  = False
        iview.use_shadow = False
        iview.activate_layer("l000")
        iview.activate_channel("l000", "scalars")

        # load data into the image view
        iview.update()

        # render the image view
        (image, depth) = Renderer.render(iview)

        # show the results
        import matplotlib.pyplot as plt
        import skimage.util
        plt.imshow(skimage.util.img_as_ubyte(image))
        plt.show()
