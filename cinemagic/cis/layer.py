from . import channel

class layer:

    def __init__(self, name):
        self.name     = name
        self.offset   = [0,0]
        self.dims     = [0,0]
        self.channels = {}

    def set_offset(self, x, y):
        self.offset = [x, y]

    def set_dims(self, w, h):
        self.dims = [w, h]

    def add_channel(self, name):
        self.channels[name] = channel.channel(name)
        self.channels[name].set_dims(self.dims[0], self.dims[1])

        return self.channels[name]

