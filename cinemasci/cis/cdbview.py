class cdbview:
    """Composible Image Set View Class
       
       Given a cinema database, this class provides access to 
       CIS data within the database.

       We note that CIS entries are expected to use Cinema's FILE column
       to record any files needed.
    """

    CISPARAMS = [   "CISImage", "CISOrigin", "CISVersion", 
                    "CISImageFlags", "CISImageWidth", "CISImageHeight", 
                    "CISLayer", "CISLayerOffsetX", 
                    "CISLayerOffsetY", "CISLayerWidth", "CISLayerHeight",
                    "CISChannel", "CISChannelVar", "CISChannelVarType", 
                    "CISChannelVarMin", "CISChannelVarMax"]

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def cis(self, value):
        self._depth = value        

    @property
    def shadow(self):
        return self._shadow

    @shadow.setter
    def cis(self, value):
        self._shadow = value        


    def __init__(self, cdb):
        self.cdb = cdb
        self.parameters = []
        self.CISParams = []

        # state
        self.images = []
        self.layers = [] 
        self.channels = {} 

        # find the CIS parameters that are in the database 
        params = cdb.get_parameter_names()
        for p in params:
            if p in cdbview.CISPARAMS: 
                self.CISParams.append(p)
            else:
                self.parameters.append(p)

        # get layer and channel information
        self.images     = self.__get_image_names()
        self.layers     = self.__get_layer_names()
        self.channels   = self.__get_channel_names()
        self._depth     = self.__query_depth()
        self._shadow    = self.__query_shadow()

    def get_cdb_parameters():
        return self.parameters

    def get_cis_parameters():
        return self.CISParameters

    def __get_image_names(self):
        query = "SELECT DISTINCT CISImage from {}".format(self.cdb.tablename)
        result = self.cdb.execute(query)

        names = []
        for row in result: 
            names.append(str(row[0]))

        return names

    def __get_layer_names(self):
        query = "SELECT DISTINCT CISLayer from {}".format(self.cdb.tablename)
        result = self.cdb.execute(query)

        names = []
        for row in result: 
            names.append(str(row[0]))

        return names

    def __get_channel_names(self):
        results = {} 

        for l in self.layers:
            results[l] = []
            query = "SELECT DISTINCT CISChannel from {} WHERE CISLayer = \'{}\'".format(self.cdb.tablename, l)
            result = self.cdb.execute(query)

            for row in result: 
                results[l].append(str(row[0]))

        return results

    def __query_depth(self):
        query = "SELECT DISTINCT CISChannel from {}".format(self.cdb.tablename)
        result = self.cdb.execute(query)

        names = []
        for row in result: 
            names.append(str(row[0]))

        return "CISDepth" in names 

    def __query_shadow(self):
        query = "SELECT DISTINCT CISChannel from {}".format(self.cdb.tablename)
        result = self.cdb.execute(query)

        names = []
        for row in result: 
            names.append(str(row[0]))

        return "CISShadow" in names 

    def get_image_layers(self, image):
        query = "SELECT DISTINCT CISLayer from {} WHERE CISImage = \'{}\'".format(self.cdb.tablename, image)
        result = self.cdb.execute(query) 

        names = []
        for row in result: 
            names.append(str(row[0]))

        return names

    def get_layer_channels(self, image, layer):
        query = "SELECT DISTINCT CISChannel from {} WHERE CISImage = \'{}\' AND CISLayer = \'{}\'".format(self.cdb.tablename, image, layer)
        result = self.cdb.execute(query) 

        names = []
        for row in result: 
            names.append(str(row[0]))

        return names


    def get_channel_extracts(self, image, layer):
        extracts = []
        for channel in self.channels[layer]:
            ext = self.get_channel_extract(image, layer, channel)
            for e in ext:
                extracts.append(e)

        return extracts

    def get_channel_extract(self, image, layer, channel):
        extracts = []
        params = {
                    "CISImage": image,
                    "CISLayer": layer,
                    "CISChannel": channel 
                 }
        extract = self.cdb.get_extracts(params)

        return extract

    #
    #
    #
    def get_image_parameters(self):
        query = "SELECT CISImageWidth, CISImageHeight from {} LIMIT 1".format(self.cdb.tablename)
        results = self.cdb.execute(query)
        data = {
                    "dims": [results[0][0], results[0][1]]
                }

        if "CISOrigin" in self.CISParams:
            query = "SELECT CISOrigin from {} LIMIT 1".format(self.cdb.tablename)
            results = self.cdb.execute(query)
        else:
            data["origin"] = "UL"

        return data

    #
    #
    #
    def get_layer_parameters(self, image, layer):
        query = "SELECT CISLayerWidth, CISLayerHeight, CISLayerOffsetX, CISLayerOffsetY from {} WHERE CISImage = \'{}\' and CISLayer = \'{}\' LIMIT 1".format(self.cdb.tablename, image, layer)
        results = self.cdb.execute(query)
        data = {
                    "dims": [results[0][0], results[0][1]], 
                    "offset": [results[0][2], results[0][3]]
               }
        return data

    #
    #
    #
    def get_channel_parameters(self, image, layer, channel):
        query = "SELECT CISChannelVar, CISChannelVarMin, CISChannelVarMax from {} WHERE CISImage = \'{}\' and CISLayer = \'{}\' and CISChannel = \'{}\' LIMIT 1".format(
                    self.cdb.tablename, image, layer, channel)
        results = self.cdb.execute(query)
        data = { 
                    "variable": {
                        "name"  : results[0][0], 
                        "range" : [results[0][1], results[0][2]]
                    }
               }

        if "CISColormap" in self.CISParams:
            query = "SELECT CISColormap, FROM {} WHERE CISImage = \'{}\' and CISLayer = \'{}\' and CISChannel = \'{}\'".format(
                        self.cdb.tablename, image, layer, channel)
            results = self.cdb.execute(query)
            data["colormap"] = results[0][0]

        else:
            data["colormap"] = { 
                                "source": "matplotlib",
                                "name"  : "gray"
                               }

        return data

