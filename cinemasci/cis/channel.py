import numpy

class channel:
    """Channel Class

    A channel is a set of values, the size of the layer that contains it (wxh) 
    and it relative to the *layer* it is a part of. 
    It can be of any type, the default if of type float. 
    A channel can contain **depth** or **lighting** information.
    A channel may reference a variable or colormap to use for rasterization.  
    """

    def __init__(self, name):
        self.name = name
        self.type = "float" 
        self.dims = [0,0]

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        shape = value.shape
        if shape[0] == self.dims[0] and shape[1] == self.dims[1]:
            self._data = value
        else:
            print("ERROR: channel data is the wrong shape")

    def set_type(self, type):
        self.type = type

    def set_dims(self, w, h):
        self.dims = [w, h]
