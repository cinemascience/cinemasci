import os

class file_writer:
    Attribute_file = "attributes.json"

    def write(self, cis):
        self.__create_toplevel_dir(cis)
        self.__write_class_metadata(cis)

    def __create_toplevel_dir(self, cis):
        status = True

        try:
            os.mkdir(cis.fname)
        except OSError:
            print("Creation of {} failed".format(cis.fname))
            status = False

        return status

    def __write_class_metadata(self, cis):
        with open(os.path.join( cis.fname, self.Attribute_file), "w") as f:
            f.write("{\n")
            f.write("  classname : \"{}\",\n".format(cis.classname))
            f.write("  dims      : [{}, {}],\n".format(cis.dims[0], cis.dims[1]))
            f.write("  version   : \"{}\",\n".format(cis.version))
            f.write("  flags     : \"{}\",\n".format(cis.flags))
            f.write("  origin    : \"{}\"\n".format(cis.origin))
            f.write("}\n")

