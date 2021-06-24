# Cinema Image Set (CIS) module

The Cinema CIS module contains classes to load, filter, render and view CIS data.

## Classes

| class | description |
|-------|-------------|
|channel        | a channel in a CIS image layer |
|cisview        | a CIS-centric view of a Cinema database. Can apply the CIS column names as filters to access CIS data |
|colormap       | a container for a colormap definition |   
|imageview      | a view of a cisview that describes an image. Contains information about the image, layers, channels, etc. to be viewed |  
|layer          | a layer in a CIS image |   
|renderer       | a renderer that takes an `imageview` as input |   
|convert.ascent | a class to convert `ascent` float output to CIS image format | 
|pynb.cis.image | a jupyter notebook image viewer for a cis image |
|pynb.cis.histogram | a jupyter notebook [image and histogram] viewer for a cis image |

## CIS Images

A CIS image is implemented by using the following classes:

- `cisview` a CIS-centric 'view' of a cinema database. 
- `imageview` a 'view' of a `cisview` that defines an image that can be rendered or otherwise analyzed. The `imageview` can load unloaded data, and can provide access to in-memory data once its view is defined.
    - `layer` a collection of data, implementing the CIS description of **layer**. A layer is metadata plus a collection of `channel` objects.
    - `channel` a collection of data, implementing the CIS description of **channel**.

## Viewing an CIS image

A database of CIS images can be viewed by the Cinema:Explorer viewer. This will show all metadata associated with the CIS database, and can be used to filter the overall database. Because the CIS images provide much more flexibility in viewing and manipulating the data, CIS python support is designed to integrate with python, providing ready access to the underlying data. In addition, the images can be rendered with the `render` class, and viewed with the `pynb.cis` classes.





