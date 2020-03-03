import unittest
import cinemagic
import pandas
import os

class TestCIS(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCIS, self).__init__(*args, **kwargs)

        self.result_dir  = "testing"
        self.result_file = "composable.cis"
        self.result_fullpath = os.path.join(self.result_dir, self.result_file)

    def test_create_hdf5(self):

        channels = ["depth", "lighting", "temperature", "pressure", "procID"]

        myCIS = cinemagic.cis.cis(self.result_fullpath)
        myCIS.set_size(1024, 768)

        ptable = pandas.read_csv("testing/data/example.csv", dtype=str, keep_default_na=False) 
        myCIS.set_parameter_table(ptable)

        myCIS.add_variable("temperature", "float", 0.0, 1000.0)
        myCIS.add_variable("pressure", "float", 0.50, 5000.0)
        myCIS.add_variable("procID", "int", 0, 1024) 

        myCIS.add_parameter("time", "float")
        myCIS.add_parameter("phi", "float")
        myCIS.add_parameter("theta", "float")
        myCIS.add_parameter("isovar", "string")
        myCIS.add_parameter("isoval", "float")

        myCIS.add_image("0000")

        image = myCIS.get_image("0000")
        layer = image.add_layer("l000")
        layer.set_offset(60, 60)
        layer.set_size(2, 2)
        for c in channels: 
            channel = layer.add_channel(c)

        layer = image.add_layer("l001")
        layer.set_offset(90, 90)
        layer.set_size(4, 4)
        for c in channels: 
            channel = layer.add_channel(c)

        layer = image.add_layer("l002")
        layer.set_offset(110, 110)
        layer.set_size(6, 6)
        for c in channels: 
            channel = layer.add_channel(c)

        # write to different storage formats 
        hdf5_writer = cinemagic.cis.write.hdf5.hdf5_writer()
        hdf5_writer.write(myCIS)

        print(myCIS.get_image_names())

        self.check_hdf5()

    def check_hdf5(self):
        assert os.path.exists(self.result_fullpath)
        os.remove(self.result_fullpath)
        assert not os.path.exists(self.result_fullpath)


if __name__ == '__main__':
    unittest.main()
