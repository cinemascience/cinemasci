

class layer:
    def __init__(self, name):
        self.name = name
        self.channels = []
        self.dims = None

class channel:
    def __init__(self):
        self.data   = None
        self.offset = None
        self.dims   = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value

    @property
    def dims(self):
        return self._dims

    @dims.setter
    def dims(self, value):
        self._dims = value

    def channels(self):
        for c in self.data:
            yield c 




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
        if value:
            self.activate_channel("CISDepth")
        else:
            self.deactivate_channel("CISDepth")

    @property
    def lighting(self):
        return self._lighting

    @lighting.setter
    def lighting(self, value):
        self._lighting = value
        if value:
            self.activate_channel("CISLighting")
        else:
            self.deactivate_channel("CISLighting")

    @property
    def cis(self):
        return self._cis

    @cis.setter
    def cis(self, value):
        self._cis = value

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

    def __init__(self, cview):
        self.active_layers = []
        self.active_channels = [] 
        self.colormaps = {}
        self.cisview = cview
        self.data = []

    def get_active_layers(self):
        for l in self.active_layers:
            yield l 

    def activate_layer(self, layer):
        if not layer in self.active_layers:
            self.active_layers.append(layer)

    def deactivate_layer(self, layer):
        if layer in self.active_layers:
            self.active_layers.remove(layer)

    def __is_active_layer(self, layer):
        return layer in self.active_layers

    def activate_channel(self, channel):
        if not channel in self.active_channels:
            self.active_channels.append(channel)

    def deactivate_channel(self, channel):
        if channel in self.active_channels:
            self.active_channels.remove(channel)

    def __is_active_channel(self, channel):
        return channel in self.active_channels

    def get_active_channels(self):
        for c in self.active_channels:
            yield c 

    def set_colormap(self, layer, colormap):
        self.colormaps[layer] = colormap

    def get_layer_data(self, layername):
        channel = self.get_active_channel(layername) 
        data = self.cis.get_image(self.image).get_layer(layername).get_channel(channel).data
        return data 

    def get_image_dims(self):
        return self.cis.dims

    def get_layer_dims(self, layername):
        return self.cis.get_image(self.image).get_layer(layername).dims 

    def get_layer_offset(self, layername):
        return self.cis.get_image(self.image).get_layer(layername).offset 

    def get_colormap(self, layername):
        return self.cis.get_colormap(self.colormaps[layername])

    def get_colormap_name(self, layername):
        return self.colormaps[layername]

    def get_active_channel(self, layername):
        return self.active_channels[layername] 

    def get_variable_range(self, layername):
        var = self.cis.get_variable(self.get_active_channel(layername))

        data = [var["min"], var["max"]] 
        if var["type"] == "float":
            data = [float(var["min"]), float(var["max"])]
        elif var["type"] == "float":
            data = [int(var["min"]), int(var["max"])]

        return data 

    def update(self):
        dimdata = self.cisview.get_image_parameters()
        self.dims = dimdata["dims"]
        for l in self.active_layers: 
            newlayer = layer(l)

            self.data.append( newlayer ) 

    def layers(self):
        for l in self.data:
            yield l 
