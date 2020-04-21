from PIL import Image

class render():

    def __init__(self):
        return

    def render(self, cis):
        return Image.new(mode="RGB", size=(cis.dims[0], cis.dims[1])) 

