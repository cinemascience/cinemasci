from . import image
from . import read
from . import write

class cis:

    Origins = ['UL', 'UR', 'LL', 'LR']

    def __init__(self, filename):
        """ The constructor. """
        self.fname          = filename
        self.classname      = "COMPOSABLE_IMAGE_SET"
        self.dims           = [0,0]
        self.flags          = "CONSTANT_CHANNELS"
        self.version        = "1.0"
        self.origin         = "UL"
        self.parameterlist  = []
        self.parametertable = None
        self.variables      = {}
        self.images         = {}
        #self.colormaps

    def debug_print(self):
        print("printing cis")
        print("  fname:     {}".format(self.fname))
        print("  classname: {}".format(self.classname))
        print("  dims:      {}".format(self.dims))
        print("  flags:     {}".format(self.flags))
        print("  version:   {}".format(self.version))
        print("  origin:    {}".format(self.origin))
        print("\n")

    def get_image(self, key):
        result = False
        if key in self.images:
            result = self.images[key]
        return result

    def get_images(self):
        for i in self.images:
            yield i

    def get_image_names(self):
        return list(self.images.keys())

    def get_origin(self):
        return self.origin

    def set_origin(self, origin):
        result = False
        if origin in self.Origins:
            self.origin = origin
            result = True;
        else:
            print("ERROR: {} is not a valid Origin value".format(origin))

        return result 

    def set_parameter_table(self, table):
        self.parametertable = table.copy(deep=True)

    def add_parameter(self, name, type):
        # check for duplicates
        self.parameterlist.append([name, type])

    def add_variable(self, name, type, min, max):
        # check for duplicates
        self.variables[name] = [type, min, max]

    def add_image(self, name):
        # check for duplicates
        self.images[name] = image.image(name)

        return self.images[name]

    def get_image(self,name):
        image = None

        if name in self.images:
            image = self.images[name]

        return image

    def set_dims(self, w, h):
        self.dims = [w, h]
