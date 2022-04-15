# Cinema Viewer Installation Module 

This module makes it easy to install cinema viewers in a variety of ways. The installation tools assume that the user knows what the final installation will look like, and therefore checks on the installation are minimal. Examples of this are given below.

Command line arguments:
- **path** The destination for the installation.
- **database** a list of databases to view with the viewer. The databases are assumed to be relative to **path**, and can be arbitrarily deep (the database needn't be the directory that is in the **path** directory). The databases need not exist at the time of the install.
- **type** type of install. One of [local, remote]. ```local``` installs all dependent libraries so that no external web access is needed. ```remote``` does not install local files, and assumes that external URLs can be accessed to load dependent libraries.
- **viewer** one of [explorer, view, simple]. This is the viewer that is installed.

```
    python3 -m cinemasci.install --path some/path --database cinema.cdb --viewer simple --type local
```

## Examples

### Single database
Assume that you would like to install ```cinema_view``` viewer in the following directory:

```
    destination/
        example.cdb/
```

An installation command could look like this, run anywhere:

```
    python3 -m cinemasci.install --path relative/path/to/destination --database example.cdb --viewer view
```

The resulting installation would look like this:

```
    destination/
        example.cdb/
        cinema/             (viewer local dependencies)
        cinema_view.html    (new viewer, pointing to example.cdb)
```

### Multiple database
Assume that you would like to install ```cinema_view``` viewer in the following directory:

```
    destination/
        example1.cdb/
        example2.cdb/
```

An installation command could look like this, run anywhere:

```
    python3 -m cinemasci.install --path relative/path/to/destination --database example1.cdb example2.cdb --viewer view
```

The resulting installation would look like this:

```
    destination/
        example1.cdb/
        example2.cdb/
        cinema/             (viewer local dependencies)
        cinema_view.html    (new viewer, pointing to example1.cdb and example2.cdb)
```

