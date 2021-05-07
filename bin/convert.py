import h5py
import numpy
import glob
import cinemasci

data = {} 
basename = "scalar_rendering"

cdbname = "pantheon.cdb"
cycles  = ["000000", "000001", "000002"]

# create the cinema database
cdb = cinemasci.new("cdb", {"path": cdbname})
cdb.initialize()

curextract = 0
for c in cycles:
    fullpath = "{}.cycle_{}".format(basename, c) 
    print(fullpath)

    for hfile in glob.glob("{}/*.hdf5".format(fullpath)):
        print("hdf5 file:")
        print("  {}".format(hfile))
        with h5py.File(hfile, "r") as bpf:
            w = bpf["coordsets/coords/dims/i"][0] - 1
            h = bpf["coordsets/coords/dims/j"][0] - 1

            print("shape")
            print("  ({}, {})".format(w, h))
            fields = bpf["fields"]
            print("fields")
            variables = ["depth", "density", "energy", "pressure"]
            for v in variables:
                # write the compressed data
                print("  {}".format(v))
                data[v] = bpf.get("fields/{}/values".format(v))[...].reshape((w,h))
                numpy.savez_compressed("{}/{}".format(cdbname, str(curextract).zfill(6)), data=data[v])

                # insert an entry in to the database
                id = cdb.add_entry({'cycle':            c, 
                                    'CISImage':         'cycle_{}'.format(c.zfill(6)), 
                                    'CISVersion':       '1.0', 
                                    'CISOrigin':        'UL', 
                                    'CISImageWidth':    w,
                                    'CISImageHeight':   h,
                                    'CISLayer':         'layer0',
                                    'CISLayerOffsetX':  0, 
                                    'CISLayerOffsetY':  0, 
                                    'CISLayerWidth':    w, 
                                    'CISLayerHeight':   h, 
                                    'CISChannel':       v, 
                                    'CISChannelVar':    v, 
                                    'CISChannelType':   'float', 
                                    'FILE':             '{}.npz'.format(str(curextract).zfill(6))})
                curextract = curextract + 1
        print("")

cdb.finalize()




