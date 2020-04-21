import numpy

class Reader:
    """ A file-based CIS Reader. """
    def __init__(self):
        return

    def read(self, cis):
        return
    
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
