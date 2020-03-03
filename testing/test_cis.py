import unittest
import cinemagic
import pandas
import os

class TestCIS(unittest.TestCase):

    def test_exercise(self):
        result_dir  = "testing"
        result_file = "composable.cis"
        result_fullpath = os.path.join(result_dir, result_file)

        channels = ["depth", "lighting", "temperature", "pressure", "procID"]

        myCIS = cinemagic.cis(result_fullpath)
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
        hdf5_writer = cinemagic.write.hdf5.hdf5_writer()
        hdf5_writer.write(myCIS)

        assert os.path.exists(result_fullpath)
        os.remove(result_fullpath)


if __name__ == '__main__':
    unittest.main()
