# CIS use cases

## Analysis and graphing of data

Because the CIS format contains data values, and not rendered pixels (RGB values, for example), the data can be used in a variety of ways. There are use cases which can specifically use the image to understand 

In this simple example, we can graph the values in a histogram, and then look at the image itself as well.

<table>
<tr>
<td>Interactive compositing. Using the depth values, a Cinema viewer can composite layers and interleave pixels from different objects, providing a more interactive visualization. In addition, .</td>
<td>
<td><img width="900" src="img/histogram_view.png"</td>
</tr>
</table>

## Interactive rendering

Using data within a CIS dataset, we can perform interactive rendering of images, providing a more flexible dataset for the viewer. The three things we can change are:

<table>
<tr>
<td>Interactive compositing. Using the depth values, a Cinema viewer can composite layers and interleave pixels from different objects, providing a more interactive visualization. In addition, .</td>
<td>
<table>
<tr>
<td><img width="300" src="img/ttk_stone.png"</td>
<td><img width="300" src="img/ttk_streamlines.png"</td>
<td><img width="300" src="img/ttk_composited.png"</td>
</tr>
<tr>
<td>Stone Layer</td>
<td>Streamline Layer</td>
<td>Composited</td>
</tr>
</table>
</td>
</tr>

<tr>
<td>Interactive control of colormaps. The images are represented as float values of variables, so we can easily apply different colormaps to the data. This allows a great deal of freedom in adjusting the post-processing visualization.</td>
<td>
<table>
<tr>
<td><img src="img/ttk_stone.png"</td>
<td><img src="img/ttk_stone_grey_colormap.png"</td>
</tr>
<tr>
<td>Warm to Cool colormap</td>
<td>Grey colormap</td>
</tr>
</table>
</td>
</tr>

<td>Interactive lighting. The images can be lit by an approximation of lighting if the data is included in the dataset.</td>
<td>
<table>
<tr>
<td><img width="300" src="img/ttk_composited.png"</td>
<td><img width="300" src="img/ttk_composited_with_shadows.png"</td>
</tr>
<tr>
<td>No shadow map</td>
<td>With shadow map</td>
</tr>
</table>
</td>
</table>


