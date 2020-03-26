from . import layer

class image:

    def __init__(self, name):
        self.name   = name
        self.layers = {} 

    def add_layer(self, name):
        self.layers[name] = layer.layer(name)

        return self.layers[name]

    def get_layers(self):
        for l in self.layers:
            yield l

    def get_layer(self, name):
        result = False
        if name in self.layers:
            result = self.layers[name]

        return result
