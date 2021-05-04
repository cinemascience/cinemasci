import os
import numpy

#
# layer class
#
class layer:
    def __init__(self, name):
        self.channel = []
        self._depth = None
        self._shadow = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        self._channel = value

    @property
    def dims(self):
        return self._dims

    @dims.setter
    def dims(self, value):
        self._dims = value

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value

    @property
    def shadow(self):
        return self._shadow

    @shadow.setter
    def shadow(self, value):
        self._shadow = value


#
# channel class
#
class channel:
    def __init__(self):
        self.data = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    def load(self, url):
        self.url = url
        if os.path.isfile(url):
            zdata = numpy.load(url)
            self.data = zdata['data']


#
# imageview class
#
class imageview:
    """ImageView Class
    A collection of settings that define a specific way of compositing the
    elements of an image. Once it is set up, the imageview's layers can
    be iterated over to return an order-dependent set of data plus colormaps
    that can be composited.
    """

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value

    @property
    def shadow(self):
        return self._shadow

    @shadow.setter
    def shadow(self, value):
        self._shadow = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def dims(self):
        return self._dims

    @dims.setter
    def dims(self, value):
        self._dims = value

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value

    def __init__(self, cview):
        self.active_layers = []
        self.active_channels = {} 
        self.cisview = cview
        self.data = {}

    def get_active_layers(self):
        return self.active_layers

    def activate_layer(self, layer):
        if not layer in self.active_layers:
            self.active_layers.append(layer)

    def deactivate_layer(self, layer):
        if layer in self.active_layers:
            self.active_layers.remove(layer)

    def __is_active_layer(self, layer):
        return layer in self.active_layers

    #
    # will activate a channel in an inactive layer
    #
    def activate_channel(self, layer, channel):
        self.active_channels[layer] = channel

    def get_layer_data(self, layer):
        channel = self.get_active_channel(layer) 
        data = self.cis.get_image(self.image).get_layer(layer).get_channel(channel).data
        return data 

    def get_image_dims(self):
        return self.cis.dims

    def get_layer_dims(self, layer):
        return self.cis.get_image(self.image).get_layer(layer).dims 

    def get_layer_offset(self, layer):
        return self.cis.get_image(self.image).get_layer(layer).offset 

    def get_active_channel(self, layer):
        results = None

        if layer in self.active_channels:
            results = self.active_channels[layer] 

        return results    

    def get_variable_range(self, layer):
        var = self.cis.get_variable(self.get_active_channel(layer))

        data = [var["min"], var["max"]] 
        if var["type"] == "float":
            data = [float(var["min"]), float(var["max"])]
        elif var["type"] == "float":
            data = [int(var["min"]), int(var["max"])]

        return data 

    def update(self):
        imdata = self.cisview.get_image_parameters()
        self.dims   = imdata["dims"]
        self.origin =  imdata["origin"]

        # TODO: error if image not set
        for l in self.active_layers:
            ldata = self.cisview.get_layer_parameters(self.image, l)
            newlayer = layer(l)
            newlayer.name = l
            newlayer.dims = ldata["dims"]
            newlayer.dims = ldata["offset"]
            self.data[l] = newlayer

            extract = self.cisview.get_channel_extract(self.image, l, self.active_channels[l])
            newchannel = channel()
            newchannel.name = self.active_channels[l]
            newchannel.load(extract[0])
            newlayer.channel = newchannel

            # load the depth map
            if self.depth:
                extract = self.cisview.get_channel_extract(self.image, l, "CISDepth") 
                newchannel = channel()
                newchannel.name = self.active_channels[l]
                newchannel.load(extract[0])
                newlayer.depth = newchannel

            # load the shadow map
            if self.shadow:
                extract = self.cisview.get_channel_extract(self.image, l, "CISShadow") 
                newchannel = channel()
                newchannel.name = self.active_channels[l]
                newchannel.load(extract[0])
                newchannel.shadow = newchannel

    def get_layer_data(self):
        return self.data
