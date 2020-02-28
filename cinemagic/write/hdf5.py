import h5py

class hdf5_writer:

    def write(self, cis):
        with h5py.File(cis.fname, "w") as f:
            f.attrs["class"]    = cis.classname
            f.attrs["size"]     = cis.size
            f.attrs["version"]  = cis.version
            f.attrs["flags"]    = cis.flags

            vlist = f.create_group("variablelist")
            for v in cis.variablelist:
                var = vlist.create_group(v)
                values = cis.variablelist[v]
                var.attrs["type"] = values[0] 
                var.attrs["min"]  = values[1]
                var.attrs["max"]  = values[2]

            self.write_cis_parameter_table(cis, f)

            imagepath = f.create_group("image")
            self.write_cis_images(cis, imagepath)


    def write_cis_parameter_table(self, cis, h5file):
        if not cis.p_table is None:
            data = cis.p_table
            table = h5file.create_group("parametertable")
            table.attrs["columns"] = ','.join(data.columns)
            table.attrs["num_rows"] = data.shape[0]
            table.attrs["num_cols"] = data.shape[1]
            cols = table.create_group("columns")
            for col in data.columns:
                cols.create_dataset( col, data=data[col].values, 
                                     dtype=h5py.string_dtype(encoding='ascii') 
                                   )

    def write_cis_images(self, cis, imagepath):
        for i in cis.images:
            curImage = cis.images[i]
            image = imagepath.create_group(curImage.name)
            layerpath = image.create_group("layer")
            self.write_image_layers(curImage, layerpath)


    def write_image_layers(self, image, layerpath):
        for l in image.layers:
            curLayer = image.layers[l]
            layer = layerpath.create_group(curLayer.name)
            layer.attrs["offset"] = str(curLayer.offset[0]) + "," + str(curLayer.offset[1])
            layer.attrs["size"]   = str(curLayer.size[0]) + "," + str(curLayer.size[1])
            channelpath = layer.create_group("channel")
            self.write_channels(curLayer, channelpath)

    def write_channels(self, layer, channelpath):
        for c in layer.channels:
            curChannel = layer.channels[c]
            channelpath.create_dataset(curChannel.name, shape=curChannel.size, data=curChannel.data)


