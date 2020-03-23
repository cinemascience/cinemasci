import unittest
import cinemagic
import pandas
import os

class TestCIS(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCIS, self).__init__(*args, **kwargs)

        self.result_dir  = 'testing'
        self.result_file = 'composable.cis'
        self.result_fullpath = os.path.join(self.result_dir, self.result_file)

    def test_create_hdf5(self):
        myCIS = cinemagic.cis.cis(self.result_fullpath)
        myCIS.set_dims(1024, 768)

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

        # write to different storage formats 
        hdf5_writer = cinemagic.cis.write.hdf5.hdf5_writer()
        hdf5_writer.write(myCIS)

        # print(myCIS.get_image_names())
        self.check_hdf5()

    def add_test_image(self, cis, imName):
        channels = ['depth', 'lighting', 'temperature', 'pressure', 'procID']

        cis.add_image(imName)
        image = cis.get_image(imName)

        layerData = {
            'l000' : {
                'offset' : [0, 10],
                'size'   : [10, 20]
            },
            'l001': {
                'offset' : [100, 110],
                'size'   : [30, 40]
            },
            'l002': {
                'offset' : [200, 210],
                'size'   : [50, 60]
            }
        }

        for l in layerData:
            layer = image.add_layer(l)
            layer.set_offset( layerData[l]['offset'][0], layerData[l]['offset'][0] )
            layer.set_size( layerData[l]['size'][0], layerData[l]['size'][0] )
            for c in channels:
                channel = layer.add_channel(c)
                channel.create_test_data()

    def check_hdf5(self):
        assert os.path.exists(self.result_fullpath)
        os.remove(self.result_fullpath)
        assert not os.path.exists(self.result_fullpath)


if __name__ == '__main__':
    unittest.main()
