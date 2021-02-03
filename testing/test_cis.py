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
import yaml

class TestCIS(unittest.TestCase):
    gold_dir     = 'testing/gold/cis'
    scratch_dir  = 'testing/scratch/cis'
    test_dir     = 'testing'

    def __init__(self, *args, **kwargs):
        super(TestCIS, self).__init__(*args, **kwargs)

        self.cur_test = ""
        self.cur_results_dir = ""

        self.result_hdf5 = 'hdf5.cis'
        self.result_hdf5_fullpath = "" 
        self.result_file = 'file.cis'
        self.result_file_fullpath = "" 
        
        self.cur_gold_dir = ""
        self.gold_hdf5 = self.result_hdf5 
        self.gold_hdf5_fullpath = "" 
        self.gold_file = self.result_file
        self.gold_file_fullpath = "" 

        self.xmlColormap = 'colormaps/blue-orange-div.xml'
        self.jsonColormap = 'colormaps/blue-1.json'

    def set_cur_test(self, test):

        self.cur_test = test

        self.cur_results_dir = os.path.join(TestCIS.scratch_dir, test)
        self.result_hdf5_fullpath = os.path.join(self.cur_results_dir, self.result_hdf5)
        self.result_file_fullpath = os.path.join(self.cur_results_dir, self.result_file)
        
        self.cur_gold_dir         = os.path.join(TestCIS.gold_dir, test)
        self.gold_hdf5_fullpath   = os.path.join(self.cur_gold_dir, self.gold_hdf5)
        self.gold_file_fullpath   = os.path.join(self.cur_gold_dir, self.gold_file)

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

        colormaps = [os.path.join(self.cur_gold_dir, 'file.cis', self.xmlColormap),
                     os.path.join(self.cur_gold_dir, 'file.cis', self.jsonColormap)]
        for c in colormaps:
            self.add_test_colormap(myCIS, c)

    def test_databases(self):
        cases = ['random', 'constant', 'linear']

        for case in cases:
            self.set_cur_test(case)
            self.__test_create_file_database()
            self.__test_create_hdf5_database()
            self.__test_create_image()
            self.__test_read_colormap_file()
            self.__test_read_file_database()
            self.__test_read_hdf5_database()

    def __test_create_file_database(self):
        myCIS = cinemasci.cis.cis(self.result_file_fullpath)
        self.__create_test_cis(myCIS)

        # write file format
        file_writer = cinemasci.cis.write.file.file_writer()
        file_writer.write(myCIS)

        # check
        self.__check_file_database()

    def __test_create_hdf5_database(self):
        myCIS = cinemasci.cis.cis(self.result_hdf5_fullpath)
        self.__create_test_cis(myCIS)

        # write hdf5 format
        hdf5_writer = cinemasci.cis.write.hdf5.hdf5_writer()
        hdf5_writer.write(myCIS)

        # check
        self.__check_hdf5_database()


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

        cis.add_image(imName)
        image = cis.get_image(imName)

        rtypes = {
            'random' : cinemasci.cis.channel.RampType.RANDOM,
            'constant' : cinemasci.cis.channel.RampType.CONSTANT,
            'linear' : cinemasci.cis.channel.RampType.LINEAR
        }
        layerData = {}
        with open(os.path.join(TestCIS.test_dir, "input", "cis", self.cur_test + ".yaml"), 'r') as lfile:
            layerData = yaml.load(lfile, Loader=yaml.FullLoader)

        layers = layerData['layers']
        for l in layers:
            layer = image.add_layer(l)
            layer.set_offset( layers[l]['offset'][0], layers[l]['offset'][1] )
            layer.set_dims( layers[l]['dims'][0], layers[l]['dims'][1] )
            for c in layers[l]['channels']:
                ch = layers[l]['channels'][c]
                channel = layer.add_channel(c)
                channel.create_test_data(rtypes[ch['type']], ch['value'])

    def __check_file_database(self):
        # is the directory there
        self.assertTrue( os.path.exists(self.result_file_fullpath) )

        # is the assets file the same
        gold = os.path.join(self.gold_file_fullpath, cinemasci.cis.write.file.file_writer.Attribute_file)
        result = os.path.join(self.result_file_fullpath, cinemasci.cis.write.file.file_writer.Attribute_file)
        self.assertTrue( filecmp.cmp( gold, result, shallow=False ) )

        # TODO check the rest of the data

        # check if colormap there
        result_xml = os.path.join(self.cur_results_dir, self.result_file, self.xmlColormap)
        result_json = os.path.join(self.cur_results_dir, self.result_file, self.jsonColormap)
        self.assertTrue(os.path.exists(result_xml))
        self.assertTrue(os.path.exists(result_json))

        # are the colormaps the same - filecmp does not have option to disregard white space
        gold_xml = os.path.join(self.cur_gold_dir, self.result_file, self.xmlColormap)
        gold_json = os.path.join(self.cur_gold_dir, self.result_file, self.jsonColormap)
        self.assertTrue( filecmp.cmp (result_xml, gold_xml, shallow=False))
        self.assertTrue( filecmp.cmp (result_json, gold_json, shallow=False))

    def __check_hdf5_database(self):
        self.assertTrue( os.path.exists(self.result_hdf5_fullpath) )

    def __test_read_file_database(self):
        self.assertTrue( os.path.exists(self.gold_file_fullpath) )
        return

    def __test_read_hdf5_database(self):
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

    def __test_read_colormap_file(self):
        pathToColormap = os.path.join(self.cur_gold_dir, 'file.cis/colormaps/blue-orange-div.xml')
        b_o_div = cinemasci.cis.colormap.colormap(pathToColormap)

        # check values read in
        self.assertTrue( b_o_div.pathToFile == os.path.join(self.cur_gold_dir, 'file.cis/colormaps/blue-orange-div.xml'))
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

    def __test_create_image(self):
        # cispath = os.path.join(TestCIS.gold_dir, "file.cis")
        cispath = os.path.join(self.cur_results_dir, "file.cis")
        cis = cinemasci.cis.cis(cispath)
        check = cinemasci.cis.read.file.cisfile(cis)
        self.assertTrue( check.verify() )

        # fname = "file.cis.dump"
        # scratch_dump = os.path.join(self.cur_results_dir, fname) 
        # gold_dump    = os.path.join(TestCIS.gold_dir,    fname) 
        # with open(scratch_dump, "w") as dumpfile:
            # check.dump(dumpfile)
        # self.assertTrue( filecmp.cmp(scratch_dump, gold_dump, shallow=False), "dump files do not match" )

        reader = cinemasci.cis.read.file.reader(cis)
        reader.read()

        iname = "render_image.png"
        render = cinemasci.cis.render.render()
        im = render.render(cis, "0000", ["l000", "l001", "l002"], ["temperature"])
        result = os.path.join(self.cur_results_dir, iname) 
        im.save(result)

        gold = os.path.join(self.cur_gold_dir, iname) 
        self.assertTrue( filecmp.cmp( gold, result, shallow=False ) )

if __name__ == '__main__':
    unittest.main()
