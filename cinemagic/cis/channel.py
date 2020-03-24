import numpy

class channel:

    def __init__(self, name):
        self.name = name
        self.type = "float" 
        self.data = None
        self.dims = [0,0]

    def set_type(self, type):
        self.type = type

    def set_dims(self, w, h):
        self.dims = [w, h]
        self.create_test_data()

    def create_test_data(self):
        self.data = numpy.random.random_sample(self.dims)
