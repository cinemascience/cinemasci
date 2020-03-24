import h5py

class Reader:

    def __init__(self):
        return

    def read(self, cis):
        with h5py.File(cis.fname, "r") as f:
            self.classname  = f.attrs["class"]
            self.dims       = f.attrs["dims"]
            self.version    = f.attrs["version"]
            self.flags      = f.attrs["flags"]
            for i in f["image"]:
                im = cis.add_image(i)
                # im.read_hdf5(f["image"][i])
