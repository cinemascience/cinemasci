import numpy
import os
import json
import glob

class cisfile():
    attrname = "attributes.json"

    def __init__(self):
        return

    def dump(self, fname):
        print(self._get_image_basedir(fname))
        print(self._get_layer_basedir(fname, "0000"))
        print(self._get_channel_basedir(fname, "0000", "l000"))
        for i in self.get_images(fname):
            print("image: {}".format(i))
            iname = os.path.basename(i)
            for l in self.get_layers(fname, iname):
                print("    layer: {}".format(l))
                lname = os.path.basename(l)
                for c in self.get_channels(fname, iname, lname):
                    print("        channel: {}".format(c))

    def get_images(self, fname):
        images = glob.glob(os.path.join(self._get_image_basedir(fname), "*"))
        for i in sorted(images):
            yield os.path.basename(i)

    def get_layers(self, fname, iname):
        layers = glob.glob(os.path.join(self._get_layer_basedir(fname, iname), "*"))
        for l in sorted(layers):
            yield os.path.basename(l)

    def get_channels(self, fname, iname, lname):
        channels = glob.glob(os.path.join(self._get_channel_basedir(fname, iname, lname), "*"))
        for c in sorted(channels):
            yield os.path.basename(c)

    def verify(self, fname):
        result = True

        if not os.path.isdir( fname ) or not os.path.isdir( self._get_image_basedir(fname) ):
            result = False

        return result

    def _get_image_basedir(self, fname):
        return os.path.join( fname, "image" )

    def _get_layer_basedir(self, fname, iname):
        return os.path.join( fname, "image", iname, "layer" )

    def _get_channel_basedir(self, fname, iname, lname):
        return os.path.join( fname, "image", iname, "layer", lname, "channel" )

    def _get_layer_dir(self, fname):
        return os.path.join( fname, "image", iname, "layer" )

    def _get_attribute_file(self, fname):
        return os.path.join( fname, cisfile.attrname ) 

    def _get_layer_attribute_file(self, fname, iname, lname):
        return os.path.join( fname, "image", iname, "layer", lname, cisfile.attrname ) 

    def _get_channel_attribute_file(self, fname, iname, lname, cname):
        return os.path.join( fname, "image", iname, "layer", lname, "channel", cname, cisfile.attrname ) 


class reader(cisfile):
    """ A file-based CIS Reader. """
    def __init__(self):
        self.cis = None
        return

    def read(self, cis):
        self.cis = cis

        # read attributes
        attrfile = self._get_attribute_file(self.cis.fname)
        attributes = self.__read_attributes(attrfile) 

        # required attributes
        self.cis.classname = attributes["classname"]
        self.cis.dims      = attributes["dims"]
        self.cis.version   = attributes["version"]
        # optional attributes
        if "flags" in attributes:
            self.cis.flags     = attributes["flags"]
        if "origin" in attributes:
            self.cis.origin    = attributes["origin"]

        for image in self.get_images( self.cis.fname ):
            self.__read_image(image)

        return
    
    def __read_image(self, iname):
        # print("    image {}".format(iname))
        newimage = self.cis.add_image(iname)

        for layer in self.get_layers( self.cis.fname, iname ):
            self.__read_layer(newimage, layer)

    def __read_layer(self, image, lname):
        newlayer = image.add_layer(lname)

        # read attributes
        attrfile = self._get_layer_attribute_file( self.cis.fname, image.name, lname )
        attributes = self.__read_attributes(attrfile) 
        # set attributes
        if "offset" in attributes:
            newlayer.offset = attributes["offset"]
        if "dims" in attributes:
            newlayer.dims   = attributes["dims"]

        for channel in self.get_channels( self.cis.fname, image.name, lname ):
            self.__read_channel(image.name, newlayer, channel)

    def __read_channel(self, iname, layer, cname):
        # print("            channel {}".format(cname))
        newchannel = layer.add_channel(cname)

        # read attributes
        attrfile = self._get_channel_attribute_file( self.cis.fname, iname, layer.name, cname )
        attributes = self.__read_attributes(attrfile) 
        # set attributes
        newchannel.type = attributes["type"]

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

