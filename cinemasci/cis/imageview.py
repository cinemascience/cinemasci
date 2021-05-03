class imageview:
    """ImageView Class
    A collection of settings that define a specific way of compositing the
    elements of an image. Once it is set up, the imageview's layers can
    be iterated over to return an order-dependent set of data plus colormaps
    that can be composited.
    """

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = value

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value

    @property
    def lighting(self):
        return self._lighting

    @lighting.setter
    def lighting(self, value):
        self._lighting = value

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

    def __init__(self):
        self.layernames = []
        self.active_channels = {}
        self.colormaps = {}

    def get_layer_names(self):
        for l in self.layernames:
            yield l 

    def activate(self, layername):
        if not layername in self.layernames:
            self.layernames.append(layername)

    def deactivate(self, layername):
        if layername in self.layernames:
            self.layernames.remove(layername)

    def __is_active(self, layername):
        return layername in self.layernames

    def set_active_channel(self, layer, channel):
        self.active_channels[layer] = channel

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

