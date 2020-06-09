from PIL import Image, ImageDraw

class render():

    def __init__(self):
        return

    def old_render(self, cis, iname, lnames, cnames):
        image = cis.get_image(iname)

        im = Image.new(mode="RGB", size=(cis.dims[0], cis.dims[1])) 
        imgfinal = ImageDraw.Draw(im)

        for layer in lnames: 
            l = image.get_layer(layer)
            if l:
                shape = [(l.offset[0], l.offset[1]), 
                        (l.offset[0] + l.dims[0], l.offset[1] + l.dims[1])]
                imgfinal.rectangle(shape, fill="#ffff33", outline="red")

        return im

    def render(self, cis, iname, lnames, cnames):
        image = cis.get_image(iname)
        imode = "RGBA"

        im = Image.new(mode=imode, size=(cis.dims[0], cis.dims[1]),
                       color=(0,0,0,0)) 

        # for now, assume only variables (no shadow, depth, etc.)
        for layer in lnames: 
            l = image.get_layer(layer)
            if l:
                limage = Image.new(mode=imode, size=(l.dims[0], l.dims[1]),
                               color=(255,255,255,255)) 
                im.paste(limage, l.offset)

        return im

