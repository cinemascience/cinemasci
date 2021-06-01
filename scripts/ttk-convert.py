import numpy
from vtk.numpy_interface import dataset_adapter as dsa
from vtk.numpy_interface import algorithms as algs
from vtk.util import numpy_support as VN

# 
# a script run in a ParaView programmable filter to extract
# float and depth data from a ttk vti image
#


data = dsa.WrapDataObject(self.GetInput())

basedir = "somedir"
arrays = ["Depth", "Elevation"]
dims = self.GetInput().GetDimensions()
print("dims : {}".format(dims))

for a in arrays:
    fname = "{}/{}.npz".format(basedir, a)
    print(fname)

    u = VN.vtk_to_numpy(data.PointData[a])
    unewshape = numpy.reshape(u, (dims[1], dims[0]))
    unewtrans = unewshape.transpose()
    unew      = numpy.fliplr(unewtrans)
    numpy.savez_compressed(fname, data=unew)

