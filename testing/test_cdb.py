import unittest
import cinemagic

class TestCIS(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCIS, self).__init__(*args, **kwargs)

    def test_create_cdb(self):
        cdb_path = "testing/data/sphere.cdb"

        cdb = cinemagic.cdb.cdb(cdb_path)
        cdb.read()
        cdb.set_extract_parameter_names(["FILE"])

        print(cdb.get_extract_pathname())

        extract = cdb.get_extract({"theta": "0", "phi": "36"})
        self.show_extract(extract)

        extract = cdb.get_extract({"phi": "36", "theta": "0"})
        self.show_extract(extract)

        extract = cdb.get_extract({"phi": "96", "theta": "0"})
        self.show_extract(extract)

    def show_extract(self, extract):
        print(extract)
