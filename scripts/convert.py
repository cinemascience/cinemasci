import cinemasci.cis.convert

inputdir  = "/Users/dhr/LANL/junk/summit/pantheon.cdb"
outputcdb = "/Users/dhr/LANL/junk/summit/test.cdb"
print("Converting:")
print("    inputdir : {}".format(inputdir))
print("    outputcdb: {}".format(outputcdb))

converter = cinemasci.cis.convert.ascent()
converter.convert(inputdir, outputcdb)
