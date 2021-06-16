import ipywidgets as widgets

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


    def display(self, image):
        import matplotlib.pyplot as plt
        import skimage.util
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # plt.figure(figsize=(1,1))
            # plt.imshow(skimage.util.img_as_ubyte(image))
            plt.figure(figsize = self.size) 
            plt.axis('off')
            plt.imshow(image, aspect=self.aspect)
            # plt.show()


