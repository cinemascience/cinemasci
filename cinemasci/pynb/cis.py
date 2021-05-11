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
        self.cdbview = cdbview
        self.sliders = ParamSliders(cdbview.get_cdb_parameters())
        return

    def display(self, image):
        import matplotlib.pyplot as plt
        import skimage.util
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # plt.figure(figsize=(1,1))
            # plt.imshow(skimage.util.img_as_ubyte(image))
            plt.imshow(image)
            plt.axis('off')
            plt.show()


