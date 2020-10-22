import unittest
import cinemasci.cis
import pandas
import os
import numpy
import shutil
import filecmp
import PIL
import sys
import json

class TestCIS(unittest.TestCase):
    gold_dir     = 'testing/gold/cis'
    scratch_dir  = 'testing/scratch/cis'

    def __init__(self, *args, **kwargs):
        super(TestCIS, self).__init__(*args, **kwargs)

        self.result_hdf5 = 'hdf5.cis'
        self.result_hdf5_fullpath = os.path.join(TestCIS.scratch_dir, self.result_hdf5)
        
        self.result_file = 'file.cis'
        self.result_file_fullpath = os.path.join(TestCIS.scratch_dir, self.result_file)
        
        self.gold_hdf5   = self.result_hdf5 
        self.gold_hdf5_fullpath = os.path.join(TestCIS.gold_dir, self.gold_hdf5)
        
        self.gold_file   = self.result_file
        self.gold_file_fullpath = os.path.join(TestCIS.gold_dir, self.gold_file)

        self.xmlColormap = 'colormaps/blue-orange-div.xml'
        self.jsonColormap = 'colormaps/blue-1.json'


    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    @classmethod
    def tearDownClass(self):
        if False:
            shutil.rmtree(TestCIS.scratch_dir)

    def __create_test_cis(self, myCIS):
        myCIS.set_dims(1024, 768)
        myCIS.set_origin("UL")

        ptable = pandas.read_csv('testing/data/sphere.cdb/data.csv', dtype=str, keep_default_na=False)
        myCIS.set_parameter_table(ptable)

        variables = [ ['temperature', 'float', 10.0, 100.0],
                      ['pressure',    'float', 20.0, 200.0],
                      ['procID',      'float', 30.0, 300.0]
                    ]
        for v in variables:
            myCIS.add_variable(v[0], v[1], v[2], v[3])

        parameters = ['time', 'phi', 'theta', 'isovar', 'isoval']
        for p in parameters:
            myCIS.add_parameter(p, 'float')

        images = ['0000', '0001', '0002']
        for i in images:
            self.add_test_image(myCIS, i)

        colormaps = [os.path.join(TestCIS.gold_dir, 'file.cis', self.xmlColormap),
                     os.path.join(TestCIS.gold_dir, 'file.cis', self.jsonColormap)]
        for c in colormaps:
            self.add_test_colormap(myCIS, c)

    def test_create_hdf5_database(self):
        myCIS = cinemasci.cis.cis(self.result_hdf5_fullpath)
        self.__create_test_cis(myCIS)

        # write hdf5 format
        hdf5_writer = cinemasci.cis.write.hdf5.hdf5_writer()
        hdf5_writer.write(myCIS)

        # check
        self.__check_hdf5_database()

    def test_create_file_database(self):
        myCIS = cinemasci.cis.cis(self.result_file_fullpath)
        self.__create_test_cis(myCIS)

        # write file format
        file_writer = cinemasci.cis.write.file.file_writer()
        file_writer.write(myCIS)

        # check
        self.__check_file_database()

    def add_test_colormap(self, cis, path):
        file_extension = os.path.splitext(path)[1]
        name = os.path.splitext(os.path.basename(path))[0]
        if (file_extension == ".xml"):
            newcolormap = cis.add_colormap(name, path)
        if (file_extension == ".json"):
            if os.path.isfile(path):
                with open(path) as jFile:
                    data = json.load(jFile)
            newcolormap = cis.add_colormap(name, data['url'])
#        name = os.path.splitext(os.path.basename(path))[0]
#        cis.add_colormap(name, path)

    def add_test_image(self, cis, imName):
        channels = ['depth', 'lighting', 'temperature', 'pressure', 'procID']

        cis.add_image(imName)
        image = cis.get_image(imName)

        layerData = {
            'l000' : {
                'offset' : [0, 10],
                'dims'   : [100, 200]
            },
            'l001': {
                'offset' : [100, 110],
                'dims'   : [250, 300]
            },
            'l002': {
                'offset' : [200, 210],
                'dims'   : [350, 400]
            }
        }

        for l in layerData:
            layer = image.add_layer(l)
            layer.set_offset( layerData[l]['offset'][0], layerData[l]['offset'][1] )
            layer.set_dims( layerData[l]['dims'][0], layerData[l]['dims'][1] )
            for c in channels:
                channel = layer.add_channel(c)
                channel.create_test_data()

    def __check_file_database(self):
        # is the directory there
        self.assertTrue( os.path.exists(self.result_file_fullpath) )

        # is the assets file the same
        gold = os.path.join(self.gold_file_fullpath, cinemasci.cis.write.file.file_writer.Attribute_file)
        result = os.path.join(self.result_file_fullpath, cinemasci.cis.write.file.file_writer.Attribute_file)
        self.assertTrue( filecmp.cmp( gold, result, shallow=False ) )

        # TODO check the rest of the data

        # check if colormap there
        result_xml = os.path.join(TestCIS.scratch_dir, self.result_file, self.xmlColormap)
        result_json = os.path.join(TestCIS.scratch_dir, self.result_file, self.jsonColormap)
        self.assertTrue(os.path.exists(result_xml))
        self.assertTrue(os.path.exists(result_json))

        # are the colormaps the same - filecmp does not have option to disregard white space
        gold_xml = os.path.join(TestCIS.gold_dir, self.result_file, self.xmlColormap)
        gold_json = os.path.join(TestCIS.gold_dir, self.result_file, self.jsonColormap)
        self.assertTrue( filecmp.cmp (result_xml, gold_xml, shallow=False))
        self.assertTrue( filecmp.cmp (result_json, gold_json, shallow=False))

    def __check_hdf5_database(self):
        self.assertTrue( os.path.exists(self.result_hdf5_fullpath) )

    def test_read_hdf5_database(self):
        self.assertTrue( os.path.exists(self.gold_hdf5_fullpath) )

        myCIS = cinemasci.cis.cis(self.gold_hdf5_fullpath)

        hdf5_reader = cinemasci.cis.read.hdf5.Reader()
        hdf5_reader.read(myCIS)

        # check values read in
        self.assertTrue( myCIS.classname == "COMPOSABLE_IMAGE_SET" )
        self.assertTrue( numpy.array_equal( myCIS.dims, [1024, 768] ) )
        self.assertTrue( myCIS.flags     == "CONSTANT_CHANNELS" )
        self.assertTrue( myCIS.version   == "1.0" )
        self.assertTrue( myCIS.origin    == "UL" )
        # myCIS.debug_print()

    def test_read_colormap_file(self):
        pathToColormap = os.path.join(TestCIS.gold_dir, 'file.cis/colormaps/blue-orange-div.xml')
        b_o_div = cinemasci.cis.colormap.colormap(pathToColormap)

        # check values read in
        self.assertTrue( b_o_div.pathToFile == os.path.join(TestCIS.gold_dir, 'file.cis/colormaps/blue-orange-div.xml'))
        self.assertTrue( b_o_div.name == 'blue-orange-div')
        #self.assertTrue( b_o_div.name == 'Divergent 1')
        self.assertTrue( len(b_o_div.points) == 47 )

    def __test_read_colormap_url(self):
        pathToColormap = 'https://raw.githubusercontent.com/cinemascience/cinemasci/master/testing/gold/cis/file.cis/colormaps/blue-orange-div.xml'
        b_o_div = cinemasci.cis.colormap.colormap(pathToColormap)
        
        # check values read in
        self.assertTrue( b_o_div.pathToFile == pathToColormap )
        self.assertTrue( b_o_div.name == 'blue-orange-div')
        #self.assertTrue( b_o_div.name == 'Divergent 1')
        self.assertTrue( len(b_o_div.points) == 47 )

    def test_create_image(self):
        cispath = os.path.join(TestCIS.gold_dir, "file.cis")
        cis = cinemasci.cis.cis(cispath)

        check = cinemasci.cis.read.file.cisfile(cis)
        self.assertTrue( check.verify() )
        fname = "file.cis.dump"
        scratch_dump = os.path.join(TestCIS.scratch_dir, fname) 
        gold_dump    = os.path.join(TestCIS.gold_dir,    fname) 
        with open(scratch_dump, "w") as dumpfile:
            check.dump(dumpfile)
        self.assertTrue( filecmp.cmp(scratch_dump, gold_dump, shallow=False), "dump files do not match" )

        reader = cinemasci.cis.read.file.reader(cis)
        reader.read()

        iname = "render_image.png"
        render = cinemasci.cis.render.render()
        im = render.render(cis, "0000", ["l000", "l001", "l002"], ["temperature"])
        result = os.path.join(TestCIS.scratch_dir, iname) 
        im.save(result)

        gold = os.path.join(TestCIS.gold_dir, iname) 
        self.assertTrue( filecmp.cmp( gold, result, shallow=False ) )

    def test_read_file_database(self):
        self.assertTrue( os.path.exists(self.gold_file_fullpath) )
        cis     = cinemasci.cis.cis(self.gold_file_fullpath)
        reader  = cinemasci.cis.read.file.reader(cis)
        reader.read()

    def test_imageview(self):
        # read a CIS file
        self.assertTrue( os.path.exists(self.gold_file_fullpath) )
        myCIS = cinemasci.cis.cis(self.gold_file_fullpath)
        file_reader = cinemasci.cis.read.file.reader(myCIS)
        file_reader.read()
        # myCIS.debug_print()

        # create an image view
        i_view = cinemasci.cis.image.imageview()
        i_view.cis = myCIS
        i_view.image = "0000"
        i_view.alpha = True
        i_view.depth = True
        i_view.lighting = True
        i_view.set_active_channel( "l000", "temperature" )
        i_view.set_colormap( "l000", "blue-orange-div" )
        i_view.set_active_channel( "l001", "pressure" )
        i_view.set_colormap( "l001", "blue-orange-div" )
        i_view.set_active_channel( "l002", "procID" )
        i_view.set_colormap( "l002", "blue-orange-div" )

        # test dimensions and offsets
        self.assertTrue(numpy.array_equal(i_view.get_image_dims(), [1024, 768]))
        self.assertTrue(i_view.get_layer_dims("l000") == [100, 200])
        # print(i_view.get_layer_dims("l000"))
        self.assertTrue(i_view.get_layer_offset("l000") == [0, 10])
        # print(i_view.get_layer_offset("l000"))

        # test activate
        i_view.activate( "l000" )
        # print("First test ...")
        for n in i_view.get_layer_names():
            self.assertTrue( n == "l000" ) 
            self.assertTrue( i_view.get_active_channel(n) == "temperature" ) 
            # print(i_view.get_layer_data(n))
            # print(i_view.get_colormap(n).points)

        # test activate/deactivate 
        i_view.activate( "l001" )
        i_view.deactivate( "l000" )
        # print("Second test ...")
        for n in i_view.get_layer_names():
            self.assertTrue( n == "l001" ) 
            self.assertTrue( i_view.get_active_channel(n) == "pressure" ) 
            # print(i_view.get_layer_data(n))
            # print(i_view.get_colormap(n).points)

    def test_imageview_example(self):
        # read a CIS file
        self.assertTrue( os.path.exists(self.gold_file_fullpath) )
        myCIS = cinemasci.cis.cis(self.gold_file_fullpath)
        file_reader = cinemasci.cis.read.file.reader(myCIS)
        file_reader.read()

        # output if you'd like to see it
        # myCIS.debug_print()

        # create an image view
        # The data here is from what we know in the test data sets
        i_view = cinemasci.cis.image.imageview()
        i_view.cis = myCIS
            # set the image ID
        i_view.image = "0000"
            # turn on or off alpha, depth and lighting
        i_view.alpha = True
        i_view.depth = True
        i_view.lighting = True
            # create active channels
            # l000
        i_view.set_active_channel( "l000", "temperature" )
        i_view.set_colormap( "l000", "blue-orange-div" )
            # l001
        i_view.set_active_channel( "l001", "pressure" )
        i_view.set_colormap( "l001", "blue-orange-div" )
            # l002
        i_view.set_active_channel( "l002", "procID" )
        i_view.set_colormap( "l002", "blue-orange-div" )

        # now, there is a set of layers and available colormaps for rendering
        # use the image view to iterate through the data like this

        # get overall dims of the image
        size = i_view.get_image_dims()

        # pre-load any colormaps, assuming you need to create your own
        # data structures before the render
        for l in i_view.get_layer_names():
            cmap = i_view.get_colormap(l)
            print(cmap.points)

        # iterate over the layers, each of which has only one active channel
        for l in i_view.get_layer_names():
            print(l)
            l_dims   = i_view.get_layer_dims(l)
            l_offset = i_view.get_layer_offset(l)
            l_data   = i_view.get_layer_data(l)
            l_cmap   = i_view.get_layer_colormap_name(l)

            # using what you know about the state, do the composite
            # composite()

if __name__ == '__main__':
    unittest.main()
