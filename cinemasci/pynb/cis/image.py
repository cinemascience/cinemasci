import ipywidgets as widgets
from cinemasci.cis.renderer import Renderer

class CISImageViewer():

    def __init__(self, cdbview):
        self.aspect      = "equal"
        self.size        = (10, 10)
        self.cdbview     = cdbview
        self.title       = ""
        self.figsize     = (1, 1)
        self.widths      = [1]
        self.height      = [1]
        return

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def widths(self):
        return self._widths

    @widths.setter
    def widths(self, value):
        self._widths = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def aspect(self):
        return self._aspect

    @aspect.setter
    def aspect(self, value):
        self._aspect = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    def display(self, iview):
        import numpy
        from matplotlib import pyplot as plt

        # update
        iview.update()

        # layers = iview.get_layer_data()
        # cdata = layers[alayer].channel.data

        fig = plt.figure(figsize=self.size, constrained_layout=True)
        spec = fig.add_gridspec(ncols=1, nrows=1, width_ratios=self.widths, height_ratios=self.height)
        fig.suptitle(self.title)

        # render the image view
        (image, depth) = Renderer.render(iview)

        # display the rendered image
        import warnings
        ax = fig.add_subplot(spec[0,0])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ax.axis('off')
            ax.imshow(image, aspect='equal')


