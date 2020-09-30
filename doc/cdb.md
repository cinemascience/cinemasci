# Cinema Database Python module (CDB)

The Cinema Database Object reads and writes Cinema specification-compliant databases. See the [current specification](https://github.com/cinemascience/cinema/blob/master/specs/dietrich/01/cinema_specD_v012.pdf) for details.

At a high level, a Cinema database is a collection of data artifacts and metadata associated with them. One uses a `cdb` object by:

1. Creating the object. The database is created with a valid path (can be written to).
2. Adding entries. The entries have the following properties:
    - They can contain `[0-n]` attributes (key, value) pairs
    - The attribute keys need not be the same for each entry
    - The attributes can be in any order
    - The entry is expected to have at least one artifact `URL`, but this is not 
      verified. It is up to the producer and the consumer of the database to handle this.
    - In order to work with Cinema viewers and current pipelines, the artifact attribute 
      should be of the form `FILE{some value}`. Again, it is up to the producer and
      consumer of the database to know about the naming scheme for the attribute columns.
3. Finalizing (writing) the object

## Example

An example of using the object looks like this:

```
import cinemasci

# create the database object
cdb = cinemasci.new("cdb", {"path": "my_database.cdb"} 

# initialize
cdb.initialize()

# add entries in any order, and with fully or partially populated attributes 
id = cdb.add_entry({'FILE02': '0002.png', 'time': '1.0', 'phi': '10.0', 'theta': '0.0'})
id = cdb.add_entry({'time': '0.0', 'phi': '0.0', 'theta': '0.0', 'FILE': '0000.png'})
id = cdb.add_entry({'time': '1.0', 'phi': '10.0', 'theta': '0.0', 'FILE01': '0001.png'})
id = cdb.add_entry({'time': '1.0', 'FILE': '0003.png'})

# finalize (writes out metadata for entries)
cdb.finalize()
```

This results in a cinema datbase with the following `data.csv` file:
```
time,phi,theta,FILE,FILE02,FILE01
1.0,10.0,0.0,,0002.png,
0.0,0.0,0.0,0000.png,,
1.0,10.0,0.0,,,0001.png
1.0,,,0003.png,,
```

## Constraints

When reading in a table, these are the steps:

1. Read a cinema table
    - a column is either a ``parameter`` or an ``extract``
2. Extract a subset of extract path columns (optional)
    - default: all extract path columns present
3. Establish an order for the extract path columns (optional)
    - default: order is the same as in the source file 
    - the order of all extract path columns establishes the ``extract path name``
    - an instance of values is an ``extract path``
4. Establish a path order for the extract path columns (optional)
    - default is the order in the source file

## Definitions

- **parameter path** A slash-separated string that defines an ordered set of parameters that designate a set of extracts.
	- Example: `/phi/theta/variable`
- **extract path** A specific instance of a *parameter path*, giving values for each parameter.
    - Example: `/0/90/temperature`

An example of data from table to path. Table read in:

| phi | theta | FILE  |
|-----|-------|-------|
|    0|      0|000.png|
|    0|     90|001.png|
|   90|      0|002.png|
|   90|     90|003.png|

The **parameter path** for this table is:

```
   /phi/theta
```

Examples of **extract path** strings, and the extracts they map to are:

```
  /0/0      000.png
  /0/90     001.png
  /90/0     002.png
  /90/90    003.png
```

A **parameter path** and an **extract path** together define a set of **key,value** pairs. In this example, you would know that a the path ``/0/90`` can be translated to values of:

- ``phi=0``
- ``theta=90``

Another **parameter path** for the same table would be to only use the ``phi`` parameter:

```
  /phi
```

This would result in multiple extracts matching each path. For example:

```
  /0        000.png,001.png
  /90       002.png,003.png
```
