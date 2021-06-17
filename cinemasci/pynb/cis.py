import ipywidgets as widgets
from cinemasci.cis.renderer import Renderer

class ParamSet():

    def __init__(self, params):
        self.params = params

    def update(self, params):
        for p in params:
            self.params[p] = params[p]

class ParamSlider():

    def __init__(self, params): 
        self.label  = widgets.Label(params["name"], style={'description_width': 'initial'})
        self.slider = widgets.IntSlider()
        self.HBox   = widgets.HBox([self.label, self.slider])
        display(self.HBox)

class ParamSliders():
    def __init__(self, params):
        self.sliders = {}

        # don't do this yet
        # for p in params: 
        #     self.sliders[p] = ParamSlider({"name": p})

class CISViewer():

    def __init__(self, cdbview):
        self.aspect  = "equal"
        self.size    = (10, 10)
        self.cdbview = cdbview
        self.sliders = ParamSliders(cdbview.get_cdb_parameters())
        return

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

    def display(self, iview, alayer):
        import numpy
        from matplotlib import pyplot as plt

        # update
        iview.update()

        layers = iview.get_layer_data()
        cdata = layers[alayer].channel.data

        fig = plt.figure(figsize=(10, 3.5), constrained_layout=True)
        widths = [2, 5]
        heights = [0.5]
        spec = fig.add_gridspec(ncols=2, nrows=1, width_ratios=widths, height_ratios=heights)
        # fig.suptitle("Here is the title of the thing")

        ax = fig.add_subplot(spec[0, 0])
        ax.hist(cdata[~numpy.isnan(cdata)], 50)
        ax.set_title("value histogram")

        # render the image view
        (image, depth) = Renderer.render(iview)

        # display the rendered image
        import warnings
        ax = fig.add_subplot(spec[0,1])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ax.axis('off')
            ax.set_title("rendered image")
            ax.imshow(image, aspect='equal')


