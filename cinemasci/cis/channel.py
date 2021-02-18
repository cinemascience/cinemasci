import numpy
from enum import Enum

class RampType(Enum):
    RANDOM = 0
    CONSTANT = 1
    LINEAR   = 2

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
        self.data = None
        self.dims = [0,0]

    def set_type(self, type):
        self.type = type

    def set_dims(self, w, h):
        self.dims = [w, h]

    def create_test_data(self, ramptype, value=0.0):

        if ramptype is RampType.RANDOM:
            numpy.random.seed(12345)
            self.data = numpy.random.random_sample(self.dims)

        elif ramptype is RampType.CONSTANT:
            self.data = numpy.full(self.dims, value)

        elif ramptype is RampType.LINEAR:
            self.data = numpy.zeros(self.dims, dtype=float)

            for w in range(self.dims[0]):
                for h in range(self.dims[1]):
                    self.data[w][h] = float(w)/float(self.dims[0])
                    



