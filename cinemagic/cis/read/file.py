import numpy
import os
import json
import glob

class reader:
    """ A file-based CIS Reader. """
    def __init__(self):
        self.attrname = "attributes.json"
        self.cis = None
        return

    def read(self, cis):
        self.cis = cis

        # read attributes
        attrfile = self.__get_attribute_file()
        attributes = self.__read_attributes(attrfile) 

        self.cis.classname = attributes["classname"]
        self.cis.dims      = attributes["dims"]
        self.cis.version   = attributes["version"]
        self.cis.flags     = attributes["flags"]
        self.cis.origin    = attributes["origin"]

        imagedir = os.path.join( self.cis.fname, "image", "*" ) 
        for image in sorted(glob.glob(imagedir)):
            imagename = os.path.basename(image)
            self.__read_image(imagename)

        return
    
    def __read_image(self, iname):
        # print("    image {}".format(iname))
        newimage = self.cis.add_image(iname)

        layerdir = os.path.join( self.cis.fname, "image", iname, "layer", "*" ) 
        for layer in sorted(glob.glob(layerdir)):
            layername = os.path.basename(layer)
            self.__read_layer(newimage, layername)

    def __read_layer(self, image, lname):
        newlayer = image.add_layer(lname)

        # read attributes
        attrfile = self.__get_layer_attribute_file( image.name, lname )
        attributes = self.__read_attributes(attrfile) 
        # set attributes
        newlayer.offset = attributes["offset"]
        newlayer.dims   = attributes["dims"]

        channeldir = os.path.join( self.cis.fname, "image", image.name, "layer", lname, "channel", "*" ) 
        for channel in sorted(glob.glob(channeldir)):
            channelname = os.path.basename(channel)
            self.__read_channel(image.name, newlayer, channelname)

    def __read_channel(self, iname, layer, cname):
        # print("            channel {}".format(cname))
        newchannel = layer.add_channel(cname)

        # read attributes
        attrfile = self.__get_channel_attribute_file( iname, layer.name, cname )
        attributes = self.__read_attributes(attrfile) 
        # set attributes
        newchannel.type = attributes["type"]

    def read_image(self, image, data):
        for l in data["layer"]:
            self.read_layer(layer, data["layer"][l])
        return

    def read_layer(self, layer, data):
        if "offset" in data.attrs.keys():
            offset = numpy.array(list(map(int, data.attrs["offset"].split(","))))
            layer.set_offset(offset[0], offset[1])
        if "dims" in data.attrs.keys():
            dims = numpy.array(list(map(int, data.attrs["dims"].split(","))))
            layer.set_dims(dims[0], dims[1])

        for c in data["channel"]:
            channel = layer.add_channel(c)
        return

    def __read_attributes(self, attrfile):
        # print("reading attributes file {}".format(attrfile))
        attributes = {}
        if os.path.isfile(attrfile):
            with open(attrfile) as afile:
                attributes = json.load(afile)
        else:
            print("ERROR loading attributes file: {}".format( attrfile ))
            exit(1)

        return attributes

    def __get_attribute_file(self):
        return os.path.join( self.cis.fname, self.attrname ) 

    def __get_layer_attribute_file(self, iname, lname):
        return os.path.join( self.cis.fname, "image", iname, "layer", lname, "attributes.json" ) 

    def __get_channel_attribute_file(self, iname, lname, cname):
        return os.path.join( self.cis.fname, "image", iname, "layer", lname, "channel", cname, "attributes.json" ) 
