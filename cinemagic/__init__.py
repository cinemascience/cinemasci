from . import image
from . import write

import h5py

class cis:

    def __init__(self, filename):
        self.fname         = filename
        self.classname     = "COMPOSABLE_IMAGE_SET"
        self.size          = [0,0]
        self.version       = "1.0"
        self.flags         = "CONSTANT_CHANNELS"
        self.parameterlist = []
        self.p_table       = None
        self.variablelist  = {} 
        self.images        = {} 


    def set_parameter_table(self, table):
        self.p_table = table.copy(deep=True)

    def add_parameter(self, name, type):
        # check for duplicates
        self.parameterlist.append([name, type])

    def add_variable(self, name, type, min, max):
        # check for duplicates
        self.variablelist[name] = [type, min, max]

    def add_image(self, name):
        # check for duplicates
        self.images[name] = image.image(name)

    def get_image(self,name):
        image = None

        if name in self.images:
            image = self.images[name]

        return image

    def set_size(self, w, h):
        self.size = [w, h]

    def read_hdf5(self, fname):
        self.fname = fname
        with h5py.File(fname, "r") as f:
            self.classname  = f.attrs["class"]
            self.size       = f.attrs["size"]
            self.version    = f.attrs["version"]
            self.flags      = f.attrs["flags"]
            for i in f["image"]:
                im = self.add_image(i)
                im.read_hdf5(f["image"][i])
