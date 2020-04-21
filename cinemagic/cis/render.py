from PIL import Image, ImageDraw

class render():

    def __init__(self):
        return

    def render(self, cis, iname, lname):
        image = cis.get_image(iname)

        im = Image.new(mode="RGB", size=(cis.dims[0], cis.dims[1])) 
        for layer in image.get_layers():
            l = image.get_layer(layer)
            shape = [(l.offset[0], l.offset[1]), 
                    (l.offset[0] + l.dims[0], l.offset[1] + l.dims[1])]
            imgfinal = ImageDraw.Draw(im)
            imgfinal.rectangle(shape, fill="#ffff33", outline="red")

        return im

