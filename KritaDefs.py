from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from krita import *


k= Krita.instance()
d = k.activeDocument()




def strSearchNReplace(string,start,stop,body):
    index = string.find(start)
    index += len(start)
    running = True
    toReplaceStr = start

    #check following character until stop sequence 
    while running:

        c = string[index]
        if c == stop[0] :
            #check if stop reached 
            sIndex = 0
            stopReached = True
            for k in stop :
                nextCIndex = index+sIndex

                if k != string[nextCIndex] and stropReached == True :
                    stopReached = False
                    sIndex+=1

            if stopReached : 
                running=False    
                break
        # add character to replace sequence
        toReplaceStr+= c
        print(c)
        index+=1
    
    
    toReplaceStr+= stop
    replaceStr = ""
    replaceStr+= start + body + stop
    print(toReplaceStr, " should be replace by ",replaceStr)
    #replace the str
    string = string.replace(toReplaceStr,replaceStr)
    
    return string



    pass

def scanLayers(layerGroup="none",lType="all", tag="none",visibility="all"):
    layersList = []
    
    if layerGroup== "none" :
        layerGroup= d.topLevelNodes()
        
        
    for layer in layerGroup:
        if (layer.visible()==visibility or visibility=="all"):
             for child in layer.childNodes():
                    layerGroup.append(child)
             if (str(layer.type())==lType or lType == "all"):
                tagI = layer.name().find(tag)
                if (tag=="none" or tagI!=-1):
                    print("layer " , layer.name(), " of type ",str(layer.type()), " was added")
                    layersList.append(layer)
                
    return layersList


        

def getColorInfo(fillayer):
        color = fillayer.filterConfig().property("color")
        #color = fillayer.filterConfig().property("")
        print(fillayer.name(),color)
	
        #need to convert xml to hexa color 
        rgbColorCode = convertXMLColorToHex(color)
        print(rgbColorCode)
        return rgbColorCode


def convertXMLColorToHex( xml):
             marks = [ "b=", "g=", "r="]
	# for r g n B inf in the xml
             beg = 28
             rgbData = []
             for colorM in marks:
		#search and stock the float info str.find(str, beg=0, end=len(string))
                
                start = xml.find(colorM , beg)
                start+=3
                floatStr = ""
                c =""
                
                while c != '\"':
                    c = xml[start] 
                    if c ==  '\"':
                        break
                    floatStr += c
                    start+=1
                print(colorM, floatStr)
                rgbData.append(float(floatStr))
             
                             #create a qcolor from RGB
             qColor= QColor()
             qColor.setRgbF(rgbData[2],rgbData[1],rgbData[0],1.0)
             #print(qColor.name(0))

             #get the hexaname of the color
             hexaCode = qColor.name(0)

             #return the heX
             return hexaCode

def vectoriseLayer(currentLayer,delete=False, cropToDocument=True):
    #set variables
    d.setActiveNode(currentLayer)
    layerName = currentLayer.name()
    print(layerName,)

    #Get opaque
    if cropToDocument:
        startFrom= "all"
        operator = "*"
    else:
        startFrom= "none"
        operator = "+"
    
    selectionOperation(startFrom,operator)


    #Create and place node
    vectorName= layerName + "_vec"
    newLayer = d.createVectorLayer(vectorName)
    print(currentLayer.parentNode().name())
    currentLayer.parentNode().addChildNode(newLayer,currentLayer)

    #Create path
    #k.action("convert_to_vector_selection").trigger()
    #time.sleep(0.4)
    k.action("convert_selection_to_shape").trigger()
    d.waitForDone()
    vectorLayer = d.activeNode()
    #for shape in d.activeNode().shapes():
           #print(shape.name())
            #print(shape.toSvg())

    #Delete old layer
    if delete : 
        currentLayer.remove()
    #time.sleep(5)
    return newLayer
            
def getVectorLayerSVG(layer,setName=True,setFillColor=False,fillColorHex="none", setStrokeColor=False, strokeColorHex = "none"):
    d.setActiveNode(layer)
    strSVG = ""
    for shape in d.activeNode().shapes():
        print("there is a shape")
        if setName :
                 shape.setName(layer.name())
        print(shape.name())
        shapeSVG=shape.toSvg()

        if setFillColor:
                #print("try to set fill color with ", fillColorHex)
                shapeSVG = strSearchNReplace(shapeSVG,"fill=\"","\"",fillColorHex)
                
        if setStrokeColor:
                shapeSVG = strSearchNReplace(shapeSVG,"stroke=\"","\"",strokeColorHex)
                

            #add new svg to svgString
        strSVG += shapeSVG
            #kop=shape.koPathShape()
            #print(shape.type())
            #print(kop.fillRule())
    return strSVG


def createSVGFile(body):

    head ="""<?xml version=\"1.0\" standalone=\"no\"?>\n
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n
<!-- Created using Krita: https://krita.org -->\n
<svg xmlns="http://www.w3.org/2000/svg"\n 
    xmlns:xlink="http://www.w3.org/1999/xlink"\n
    xmlns:krita="http://krita.org/namespaces/svg/krita"\n
    xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"\n
    width="628.8pt"\n
    height="628.8pt"\n
    viewBox="0 0 628.8 628.8">\n
<defs/>\n
"""
    end= """</svg>"""
    svgStr = head+body+end
    return svgStr


def saveTxtToFile(txt, name, format=".txt", writingMethod ="a" ):
    fileName= name+format
    file = open(fileName, writingMethod)
    file.write(txt)
    print(fileName, "written")

                
def getSvgFromFillLayers(keepVectorLayer = False):
    #Catch all filllayer and turn them into an svg file
    toVectorise =[]
    toVectorise = scanLayers("none","filllayer","none",True)
    svgBody=""

    for layer in toVectorise:
        fillColorHex = getColorInfo(layer)
        #print("the color info sent is", fillColorHex )
        vectorLayer = vectoriseLayer(layer,delete=False)
        layerSVG = getVectorLayerSVG(vectorLayer,True,True,fillColorHex,True)
        svgBody+= layerSVG
        if not keepVectorLayer:
            vectorLayer.remove()
    
    svg = createSVGFile(svgBody)
    print("creating svg of document ", d.fileName())
    saveTxtToFile(svg,d.fileName(),".svg")

    def updateChild(childTag = "C:",parentTag = "P:"):    
       
        # create selection    
        childMasks = scanLayers("none","transparencymask",childTag,"all")
        parentMasks = scanLayers("none","transparencymask",parentTag,"all")
        
        for child in childMasks:

            childNewAlpha = Selection()
            reverse = False
            name=child.name()
            setName = False
            parentName=parentTag
            key = ""
            
            
            for i in range (len(childTag),len(name)):
                c= name[i]
                print(c)
                if i==len(childTag):
                    if name[i]=="-":
                        key="-"
                        k.action("select_all").trigger()
                        print("selectAll")
                        d.waitForDone()
                    else:
                        key="+"
                        k.action("select_all").trigger()
                        d.waitForDone()
                    childNewAlpha = d.selection()
                elif operators.get(c) != None:
                    if setName==True:
                        #on recupère le calque parent
                        parentLayer = d.nodeByName(parentName)
                        #on set la selection sur childalpha
                        d.setSelection(childNewAlpha)
                        #on applique la bonne fonction  à la selection
                        action = "selectopaque_"
                        action += operators.get(key)
                        k.action(action).trigger()
                        d.waitForDone()

                        print(action, key)
                        

                        #On remplace les alpaha du calque
                        
                        #on reinitialise les variables
                        parentName ="P:"
                    key = c
                    setName=True
                else : 
                    
                    setName=True
                    parentName+=c
            
            replaceAlpha(name,childNewAlpha)
            d.waitForDone()
            d.refreshProjection()

                

            #On lit un a un les caractère de la chaine de cara        
            #Si le caractère existe comme clef du dico operator, on set





def replaceAlpha(layerName, selection):
        k.action("reset_fg_bg").trigger()
        d.waitForDone()
        layer = d.nodeByName(layerName)
        active = d.setActiveNode(layer)

        #Empty layer Mask
        action("select_all").trigger()
        d.waitForDone()
        k.action("fill_selection_background_color").trigger()
        d.waitForDone()

        #Apply selection as alpha
        d.setSelection(selection)
        k.action("fill_selection_foreground_color").trigger()
        d.waitForDone()





def selectionOperation(startFrom="none",operator="+"):
    operators = {
    "+":"_add",      #add
    "-":"_subtract",   #subtract
    "*":"_intersect",        #intersect    
    }


    k.action("select_all").trigger()
    d.waitForDone()
    
    action = "selectopaque"+ operators.get(operator)

    k.action(action).trigger()
    d.waitForDone()
    return d.selection()

def getLayerPrefix(layer, getAlphaInherit = False):
    prefix=""
    name = layer.name()

    #search for prefix
    for c in name:
        if c != "-" and c != "@":
            try:
                int(c)
            except ValueError:
                break
        
        if c == "@" and not getAlphaInherit:
            break
        prefix += c
    return prefix


def setLayerPrefix ( layer, numerotate = True, inheritateA = True ):
    newPrefixe=""
    

    name = layer.name()

    #search for old naming
    oldPrefix = getLayerPrefix( layer, True)
    print( "oldprefixe is ", oldPrefix )

    #search for parent prefix
    parent = layer.parentNode()

    parentPrefix=""
    if parent != 0: #if parent isn't root
        parentPrefix = getLayerPrefix(parent)
    
    newPrefixe += parentPrefix

    #get layer position in parent
    reverseI = 0
    maxI = 0

    for siblings in parent.childNodes():
        if siblings.visible():
            maxI += 1
        if siblings == layer:
            reverseI = maxI
    

    
    index = (maxI - reverseI)+1 
    newPrefixe += str(index)
    newPrefixe += "-"

    if inheritateA and layer.inheritAlpha():
        newPrefixe += "@"
    
    if oldPrefix != "":
        newName = name.replace( oldPrefix, newPrefixe)
    else:
        newName = newPrefixe + name
    layer.setName(newName)

    

        



#newSelection = newSelection.intersect(d.selection())
#d.setSelection(newSelection)
# ACTION
layers = scanLayers(layerGroup="none",lType="all", tag="none",visibility = True)
for layer in layers:
    setLayerPrefix(layer)
#getSvgFromFillLayers()
