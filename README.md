# BlKrTb
Toolbox to ease a propduction pipeline between krita and blender grease pencil

For the moment it's only two collections of python fonctions that could be use respectivly in Krita and Blender for this purpose
This is not user friendly, and you would probably not be able to use it without getting into the code and understant it.

Here is a list of the things you could expect to do with both collections.

KritaDefs.py:
  °Auto convert paint layer in fill layer
  °Auto convert Fill layers into VectorLayers  
  °Auto Rename layers depending on they place in the hierarchi tree and the alph inheritancy
  °Auto export Filllayers to a .svg file, with name, color and stroke informations ( color export is buggy,hue and saturation OK, but value is way too low)
  Draft
  °Automatically upload a child alpha based on one or several parents alpha and operators (draft/buggy)
  
 BlenderDefs.py:
 °place all the curves imported as SVG into a single Gpencil or more based on parameters, with an autorename, and an auto masking dependin
  
