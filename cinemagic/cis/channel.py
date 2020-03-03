import numpy

class channel:

    def __init__(self, name):
        self.name = name
        self.type = "float" 
        self.data = None
        self.size = [0,0]

    def set_type(self, type):
        self.type = type

    def set_size(self, w, h):
        self.size = [w, h]
        self.create_test_data()

    def create_test_data(self):
        self.data = numpy.random.random_sample(self.size)
