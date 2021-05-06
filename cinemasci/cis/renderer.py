import numpy as np


class Renderer:

    def __init__(self):
        return

    # Paste buffer 'src' to buffer 'dest' at the 'offset' assuming dest is
    # large enough.
    @staticmethod
    def paste(dest, src, offset):
        ends = offset + src.shape
        # TODO: check on ends[] such that it actually fits. Does numpy
        #  automatically do this?
        dest[offset[0]:ends[0], offset[1]:ends[1], :] = src
        return dest

    # Color a scalar value buffer 'scalars' by the 'colormap'
    @staticmethod
    def color(scalars, colormap):
        # TODO: this is an NOP, replace it with the real stuff
        image = np.zeros((scalars.shape[0], scalars.shape[1], 3))
        image[:, :, 0] = scalars
        return image

        # values = colormap[:, 0]
        # rgbs = colormap[:, 2:]
        # cmap_fn = interp1d(values, rgbs, axis=0)
        # return cmap_fn(scalars)

    @staticmethod
    def blend(dest, src, mask):
        dest[mask] = src[mask]

    @staticmethod
    def depth_composite(dest_color, dest_z, src_color, src_z):
        mask = np.nan_to_num(dest_z, nan=np.inf) > \
               np.nan_to_num(src_z, nan=np.inf)
        Renderer.blend(dest_color, src_color, mask)
        Renderer.blend(dest_z, src_z, mask)

    def render(self, iview):

        # FXIME: this assumes RGB rather than RGBA color
        canvas = np.zeros((iview.dims[0], iview.dims[1], 3), float)
        depth = np.ones((iview.dims[0], iview.dims[1])) * np.inf

        # TODO: how to make use of 'origin'?
        layers = iview.get_layer_data()
        for name, layer in layers.items():
            # TODO: where is the actual predefined colormaps aka. cis.colormaps?
            data = layer.channel.data
            colored = Renderer.color(data, layer.channel.colormap)
            rectangle = [
                slice(layer.offset[0], layer.offset[0] + data.shape[0]),
                slice(layer.offset[1], layer.offset[1] + data.shape[1])]
            if iview.use_depth:
                Renderer.depth_composite(canvas[tuple(rectangle)],
                                         depth[tuple(rectangle)],
                                         colored, layer.depth.data)
            else:
                canvas = Renderer.paste(canvas, colored, layer.offset)
        # iview.dims is in row by column rather than x-dims by y-dims,
        # we need to transpose the two axes.
        return canvas.transpose((1, 0, 2)), depth.T
