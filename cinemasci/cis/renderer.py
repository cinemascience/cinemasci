import numpy as np
from scipy.interpolate import interp1d


class Renderer:

    def __init__(self):
        return

    # Paste buffer 'src' to buffer 'dest' at the 'offset' assuming dest is
    # large enough.
    @staticmethod
    def paste(dest, src, offset):
        ends = offset + src.shape
        dest[offset[0]:ends[0], offset[1]:ends[1], :] = src
        return dest

    # Color a scalar value buffer 'scalars' by the 'colormap'
    @staticmethod
    def color(scalars, colormap):
        cmap_fn, values = Renderer.make_rgb_colormap(colormap)
        # rescale scalars to be within the range of the colormap
        scalars = (scalars - np.nanmin(scalars)) / \
                  (np.nanmax(scalars) - np.nanmin(scalars))
        scalars = values.min() + scalars * (values.max() - values.min())
        return cmap_fn(scalars)

    @staticmethod
    def make_rgb_colormap(colormap):
        assert colormap['colorspace'] == 'rgb'
        points = colormap['points']
        values = np.zeros(len(points))
        rgbs = np.zeros((len(points), 3))
        for i in range(len(points)):
            values[i] = points[i]['x']
            rgbs[i, 0] = points[i]['r']
            rgbs[i, 1] = points[i]['g']
            rgbs[i, 2] = points[i]['b']
        cmap_fn = interp1d(values, rgbs, axis=0)
        return cmap_fn, values

    @staticmethod
    def blend(dest, src, mask):
        dest[mask] = src[mask]

    @staticmethod
    def depth_composite(dest_color, dest_z, src_color, src_z):
        mask = np.nan_to_num(dest_z, nan=np.inf) > \
               np.nan_to_num(src_z, nan=np.inf)
        Renderer.blend(dest_color, src_color, mask)
        Renderer.blend(dest_z, src_z, mask)

    @staticmethod
    def render(iview):

        # FXIME: this assumes RGB rather than RGBA color
        canvas = np.zeros((iview.dims[0], iview.dims[1], 3), float)
        depth = np.ones((iview.dims[0], iview.dims[1])) * np.inf

        # TODO: how to make use of 'origin'?
        layers = iview.get_layer_data()
        for name, layer in layers.items():
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
