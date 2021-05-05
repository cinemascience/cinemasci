from IPython.display import Image

class render():

    def __init__(self):
        self.file = "CISExampleImage.png"

    #
    # render an iview object
    #
    def render(self, iview):
        # this is a dummy renderer - it simply returns an image
        image = Image(filename=self.file)

        return image
