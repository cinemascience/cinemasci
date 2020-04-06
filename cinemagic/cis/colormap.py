import xml.etree.ElementTree as ET
#from urllib.request import urlopen
#import requests

class colormap:
    """Colormap Class
    A layer is a collection of values that comprise of the colormap. 
    A colormap is usually a list of object, each object in the form (x, r, g, b) where x is a value 
    0 and 1 and r,g,b normalized values between zero and one that correspond to the red, green and blue 
    color channels. 
    Are we considering alpha channels in colormaps?
    What is the dimension of a colormap?
    """

    def __init__(self, pathToXML):
        """Colormap constructor"""
        self.pathToXML = pathToXML
        self.name = ""
        self.points = []
        
        # these attributes are not guaranteed
        #self.startIndex = 0
        #self.endIndex = 1
        #self.startPos = 0
        #self.endPos = 1
        #self.startValue = 0
        #self.endValue = 1
        #self.startAlpha = 1
        #self.endAlpha = 1
        #self.flipped = False
        
        tree = ET.parse(pathToXML)
        root = tree.getroot()
        for cmap in root.findall('ColorMap'):
            self.name = cmap.get('name')

        for point in root.iter('Point'):
            value = point.get('x')
            alpha = point.get('o')
            red   = point.get('r')
            green = point.get('g')
            blue  = point.get('b')
            self.points.append((float(value), float(alpha),
                                float(red), float(green), float(blue)))
