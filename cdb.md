# Python modules for Cinema

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




