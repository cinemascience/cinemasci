from . import layer

class image:

    def __init__(self, name):
        self.name   = name
        self.layers = {} 

    def add_layer(self, name):
        self.layers[name] = layer.layer(name)

        return self.layers[name]
