import numpy as np
import skimage.color
from scipy.interpolate import interp1d


def paste(x, y, offset):
    dims = y.shape
    x[offset[0]:(offset[0] + dims[0]), offset[1]:(offset[1] + dims[1]), :] = y
    return x


def depth_composite(a, depth_a, b, depth_b):
    mask = depth_a < depth_b
    composited = b
    composited[mask] = a[mask]
    return composited


class render():

    def __init__(self):
        return

    def render(self, cis, iname, lnames, cnames):
        image = cis.get_image(iname)

        result = np.zeros((cis.dims[1], cis.dims[0], 3))
        points = cis.colormaps['blue-1'].get_points()
        colormap = np.asarray(points)

        values = colormap[:, 0]
        rgbs = colormap[:, 2:]
        cmap = interp1d(values, rgbs, axis=0)
        # for now, assume only variables (no shadow, depth, etc.)
        for layer in lnames:
            l = image.get_layer(layer)
            if l:
                arr = cmap(l.get_channel(cnames[0]).data)
                result = paste(result, arr, l.offset)

        return result
