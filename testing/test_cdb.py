import unittest
import cinemagic

class TestCIS(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCIS, self).__init__(*args, **kwargs)

    def test_create_cdb(self):
        # test failing to load a cdb that doesn't exist
        cdb_path = "testing/data/not_there.cdb"
        cdb = cinemagic.cdb.cdb(cdb_path)
        self.assertFalse(cdb.read())

        # testing a single extract database
        cdb_path = "testing/data/sphere.cdb"
        cdb = cinemagic.cdb.cdb(cdb_path)
        self.assertTrue(cdb.read())
        cdb.set_extract_parameter_names(["FILE"])

        # test pathname
        self.assertEqual(cdb.get_extract_pathname(), "/theta/phi")

        # test the same query with parameters in different order
        extract = cdb.get_extract({"theta": "0", "phi": "36"})
        self.assertEqual(extract, "testing/data/sphere.cdb/image/36/0.png")
        extract = cdb.get_extract({"phi": "36", "theta": "0"})
        self.assertEqual(extract, "testing/data/sphere.cdb/image/36/0.png")

        # test a negative query (doesn't exist)
        extract = cdb.get_extract({"phi": "96", "theta": "0"})
        self.assertEqual(extract, None)
