import numpy
import os
import json

class reader:
    """ A file-based CIS Reader. """
    def __init__(self):
        self.attributes = {}
        return

    def read(self, cis):

        self.__read_attributes(cis)

        return
    
    def __read_attributes(self, cis):
        attrfile = os.path.join( cis.fname, "attributes.json")
        if os.path.isfile(attrfile):
            with open(attrfile) as afile:
                self.attributes = json.load(afile)
        else:
            print("ERROR loading attributes file: {}".format( attrfile ))
            exit(1)

        cis.classname = self.attributes["classname"]
        cis.dims      = self.attributes["dims"]
        cis.version   = self.attributes["version"]
        cis.flags     = self.attributes["flags"]
        cis.origin    = self.attributes["origin"]

    def read_image(self, image, data):
        for l in data["layer"]:
            self.read_layer(layer, data["layer"][l])
        return

    def read_layer(self, layer, data):
        if "offset" in data.attrs.keys():
            offset = numpy.array(list(map(int, data.attrs["offset"].split(","))))
            layer.set_offset(offset[0], offset[1])
        if "dims" in data.attrs.keys():
            dims = numpy.array(list(map(int, data.attrs["dims"].split(","))))
            layer.set_dims(dims[0], dims[1])

        for c in data["channel"]:
            channel = layer.add_channel(c)
        return
