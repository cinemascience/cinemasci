import unittest
import cinemagic
import pandas
import os
import numpy
import shutil

class TestCIS(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCIS, self).__init__(*args, **kwargs)

        self.result_dir  = 'testing'
        self.result_hdf5 = 'hdf5.cis'
        self.result_hdf5_fullpath = os.path.join(self.result_dir, self.result_hdf5)

        self.result_file = 'file.cis'
        self.result_file_fullpath = os.path.join(self.result_dir, self.result_file)

        self.gold_dir    = 'testing/gold'
        self.gold_hdf5   = 'hdf5.cis'
        self.gold_hdf5_fullpath = os.path.join(self.gold_dir, self.gold_hdf5)

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def tearDown(self):
        if os.path.exists(self.result_hdf5_fullpath):
            os.remove(self.result_hdf5_fullpath)
        self.assertFalse( os.path.exists(self.result_hdf5_fullpath) )

        if os.path.exists(self.result_file_fullpath):
            shutil.rmtree(self.result_file_fullpath)
        self.assertFalse( os.path.exists(self.result_file_fullpath) )

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

    def test_create_hdf5(self):
        myCIS = cinemagic.cis.cis(self.result_hdf5_fullpath)
        self.__create_test_cis(myCIS)

        # write hdf5 format
        hdf5_writer = cinemagic.cis.write.hdf5.hdf5_writer()
        hdf5_writer.write(myCIS)
        self.__check_hdf5()

    def test_create_file(self):
        myCIS = cinemagic.cis.cis(self.result_file_fullpath)
        self.__create_test_cis(myCIS)

        # write file format
        file_writer = cinemagic.cis.write.file.file_writer()
        file_writer.write(myCIS)

        self.__check_file()

    def add_test_image(self, cis, imName):
        channels = ['depth', 'lighting', 'temperature', 'pressure', 'procID']

        cis.add_image(imName)
        image = cis.get_image(imName)

        layerData = {
            'l000' : {
                'offset' : [0, 10],
                'dims'   : [10, 20]
            },
            'l001': {
                'offset' : [100, 110],
                'dims'   : [30, 40]
            },
            'l002': {
                'offset' : [200, 210],
                'dims'   : [50, 60]
            }
        }

        for l in layerData:
            layer = image.add_layer(l)
            layer.set_offset( layerData[l]['offset'][0], layerData[l]['offset'][1] )
            layer.set_dims( layerData[l]['dims'][0], layerData[l]['dims'][1] )
            for c in channels:
                channel = layer.add_channel(c)
                channel.create_test_data()

    def __check_file(self):
        self.assertTrue( os.path.exists(self.result_file_fullpath) )

    def __check_hdf5(self):
        self.assertTrue( os.path.exists(self.result_hdf5_fullpath) )

    def test_read_hdf5(self):
        self.assertTrue( os.path.exists(self.gold_hdf5_fullpath) )

        myCIS = cinemagic.cis.cis(self.gold_hdf5_fullpath)

        hdf5_reader = cinemagic.cis.read.hdf5.Reader()
        hdf5_reader.read(myCIS)

        # check values read in 
        self.assertTrue( myCIS.classname == "COMPOSABLE_IMAGE_SET" )
        self.assertTrue( numpy.array_equal( myCIS.dims, [1024, 768] ) )
        self.assertTrue( myCIS.flags     == "CONSTANT_CHANNELS" )
        self.assertTrue( myCIS.version   == "1.0" )
        self.assertTrue( myCIS.origin    == "UL" )
        # myCIS.debug_print()


if __name__ == '__main__':
    unittest.main()
