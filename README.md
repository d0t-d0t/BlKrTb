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
  

# LIST OF KRITA'S FUNCTION

## COMPLEX KRITA FUNCTION

def getSvgFromFillLayers(keepVectorLayer = False):
  * get the svg of all the fill layer saved in a file, with the colordata passed 
   this part is buggy as color are way to dark for the moment
  
## SIMPLE KRITA FUNCTION



def cleanFillLayer(fillLayer,threshold = True, tValue = 128):
  * remove any pixel informations from outside the document area
  can apply a threshold to sharp edges 
  if so, remove pixel painted under the given value
    


def getColorInfo(fillayer)->str: 
  * return the color of a filllayer as '#xxxxxx' str



def getLayerPrefix(layer, getAlphaInherit = False) -> str :
  * get the prefix of a layer in the form "1-1-n(...)n-@" as str



def getVectorLayerSVG(layer,setName=True,setFillColor=False,fillColorHex="none", setStrokeColor=False, strokeColorHex = "none"):
    * Get the svg body of a vector layer
    possibility to override stroke and fill status and color



def replaceAlpha(layerName, selection): 
    * replace the alpha of a filllayer concidering a selection            


def scanLayers(layerGroup="none",lType="all", tag="none",visibility="all"):
  * return a list of layer based on a serie of filter:
  from a layer group or every layers if "none"
  from a specified type
  having specific str in their name
  from visible or not or all
  
  
  ## PYTHON FUNCTION


def convertXMLColorToHex( xml:str) -> str:
   * convert an xml color to an hexa code "#xxxxxx"

def createSVGFile(body): 
   * add header  and end blises to a svg body

def saveTxtToFile(txt, name, format=".txt", writingMethod ="a" ): 
   * save a str into a file

def strSearchNReplace(string : str, start : str, stop : str, body : str) -> str: 
   * replace in a str a sequence by another


