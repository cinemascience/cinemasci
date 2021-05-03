

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

    def __init__(self, cdb):
        self.cdb = cdb
        self.parameters = []
        self.CISParams = []

        # state
        self.image = None
        self.layers = [] 
        self.channels = [] 

        # find the CIS parameters that are in the database 
        params = cdb.get_parameter_names()
        for p in params:
            if p in cdbview.CISPARAMS: 
                self.CISParams.append(p)
            else:
                self.parameters.append(p)

    def set_image(self, i):
        #TODO error check
        self.image = i

    def set_layers(self, layers):
        #TODO error check
        self.layers = layers

    def set_channels(self, channels):
        #TODO error check
        self.channels = channels

    def get_cdb_parameters():
        return self.parameters

    def get_cis_parameters():
        return self.CISParameters

    def get_image_names(self):
        query = "SELECT DISTINCT CISImage from {}".format(self.cdb.tablename)
        result = self.cdb.execute(query)

        names = []
        for row in result: 
            names.append(str(row[0]))

        return names

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


    def get_extracts(self, params):

        extracts = []
        for l in self.layers:
            for c in self.channels:
                params["CISLayer"] = l 
                params["CISImage"] = self.image
                params["CISChannel"] = c

                ext = self.cdb.get_extracts(params)

                for e in ext:
                    extracts.append(e)

        return extracts

    #
    #
    #
    def get_image_parameters(self):
        query = "SELECT CISImageWidth, CISImageHeight from {} WHERE CISImage = \'{}\' LIMIT 1".format(self.cdb.tablename, self.image)
        results = self.cdb.execute(query)
        data = {
                    "dims": [results[0][0], results[0][1]]
                }

        return data

    #
    #
    #
    def get_layer_parameters(self, layer):
        query = "SELECT CISLayerWidth, CISLayerHeight, CISLayerOffsetX, CISLayerOffsetY from {} WHERE CISImage = \'{}\' and CISLayer = \'{}\' LIMIT 1".format(self.cdb.tablename, self.image, layer)
        results = self.cdb.execute(query)
        data = {
                    "dims": [results[0][0], results[0][1]], 
                    "offset": [results[0][2], results[0][3]]
               }
        return data

    def get_channel_parameters(self, layer, channel):
        query = "SELECT CISChannelVar, CISChannelVarMin, CISChannelVarMax from {} WHERE CISImage = \'{}\' and CISLayer = \'{}\' and CISChannel = \'{}\' LIMIT 1".format(
                    self.cdb.tablename, self.image, layer, channel)
        results = self.cdb.execute(query)
        data = { 
                    "variable": results[0][0], 
                    "range"   : [results[0][1], results[0][2]]
                }

        return data

