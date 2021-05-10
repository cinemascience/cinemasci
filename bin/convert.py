import h5py
import numpy
import glob
import cinemasci

data = {} 
basename = "pantheon_output"

cdbname = "pantheon.cdb"
cycles  =   [
                "000000", "000010", "000020", "000030", "000040", "000050", "000060", "000070", "000080", "000090",         
                "000100", "000110", "000120", "000130", "000140", "000150", "000160", "000170", "000180", "000190",         
                "000200", "000210", "000220", "000230", "000240", "000250", "000260", "000270"
            ] 

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

                channel = v
                if channel is 'depth':
                    channel = 'CISDepth'
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
                                    'CISChannel':       channel, 
                                    'CISChannelVar':    v, 
                                    'CISChannelType':   'float', 
                                    'FILE':             '{}.npz'.format(str(curextract).zfill(6))})
                curextract = curextract + 1
        print("")

cdb.finalize()




