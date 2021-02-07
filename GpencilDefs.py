import bpy


prefixDic = {
    '-' : "sub",
    '@' : "alphaInherit"
}

def curveAsGPencil( keepOriginal = False, searchForIdentifier = True  ):
    identifierStop = "-"

    #Import svg file as curve
    #List all curves of the document
    curvesKeysList = bpy.data.curves.keys()
    curvesKeysList.sort(reverse=True)
    print(curvesKeysList)
    #for each curve
    for key in curvesKeysList:
        
        #Store the name
        print(key)
        layerName = key+"_lay"   
        
        # Get the identifier
        stopIndex = layerName.find("-")
        print(stopIndex)
        
        identifier = ""
        if searchForIdentifier:
            if stopIndex != -1 :
                i = 0
                while i != stopIndex :
                    identifier += layerName[i]
                    i += 1
            else : 
                identifier = layerName
        else:
            identifier = "root"
        print(identifier)
        
        #set current curve as selected  
        cur = bpy.context.scene.objects[key]       # Get the object
        bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
        bpy.context.view_layer.objects.active = cur   # Make the cube the active object 
        cur.select_set(True)
        

        #convert the curve as GP
        bpy.ops.object.convert(target='GPENCIL',keep_original = keepOriginal)
        
        #get the grease pencil
        gP = bpy.context.scene.objects["GPencil"]
        gPL = gP.data.layers["GP_Layer"]
        gPL.info = layerName
        #set the name of the GP layewr
        #set the material name

        #If there is no GP for this identi
        try :
            parentGP = bpy.context.scene.objects[identifier]
            #set the current GP name as "identifier"
        except KeyError:
            gP.name = identifier
        else:                
        #If there is already a GP for this identifier
            
            #make the right GP selected
            bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
            bpy.context.view_layer.objects.active = gP   # Make gp the active object 
           

            


            #passer en editmode
            
            bpy.ops.gpencil.editmode_toggle()
            print(bpy.context.mode)
            
            

            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    override = bpy.context.copy()
                    override['area'] = area
                    #selectionner tout les points
                    bpy.ops.gpencil.select_all({"area" : area}, action="SELECT")
                    
                    #copier les points
                    bpy.ops.gpencil.copy({"area" : area})
                    
                    break

            
            #passer en object mode 
            bpy.ops.gpencil.editmode_toggle()
            bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
            #select parentGP
            bpy.context.view_layer.objects.active = parentGP
            #create new layer
            bpy.ops.gpencil.layer_add()
            parentGP.data.layers["GP_Layer"].info = layerName

            
            #paste strokes
            bpy.ops.gpencil.paste({"area" : area},type='ACTIVE')
            
            #frameToPaste = gPL.frames[0].copy()
            bpy.data.objects.remove(gP)
                
def getPrefix(gpLayer):#return the prefix of a GPLayer
    prefix = ""    
    name = gpLayer.info

    #search for prefix
    for c in name:
        if c not in prefixDic.keys():
            try:
                int(c)
            except ValueError:
                break
        
        prefix += c
    return prefix

def getLayerFromPrefix(gP,prefix):
    hasResult=False
    print ("searching for layer", prefix)
    layerList = gP.data.layers.keys()
    for key in layerList :
        layerName = key
        prefixIndex= layerName.find(prefix)
        if layerName.find(prefix) == 0: #break may cause trouble in case it get level below first
            hasResult=True
            #print("it exist")
            # need yo check if its a same level layer!
            nextCIndex = len(prefix) + 1
            c = key[nextCIndex]
            if c not in prefixDic.keys():
                try:
                    int(c)
                except ValueError:
                    #print("layer " , key, "mays be used as mask")
                    return gP.data.layers[key]  
                    
                    #break 
                else: 
                    print("this layer isn't on the same level")
                    
                              
    #check if there was result  
    if hasResult:
        return "pass"      
    else:
        return "none"




def getRelativesFromPrefix( holdingGP, startingPrefix, parentingLevel = 0, above = True, behind = True):#
    
    relativesList = []    

    splitedStartingPrefix  = startingPrefix.split("-")
    #remove the "" entry
    splitedStartingPrefix.remove("")
    print("the sptited prefix is" , splitedStartingPrefix)
    
    mIndex = len(splitedStartingPrefix) - (parentingLevel+1)
    splitedPrefixToGet = splitedStartingPrefix

    #read string from mast char

    
    #for each level pass a "-"
    #placeholder in the prefixtoget


    loopIndex = 2 
    operator = 0

    #bug sur cette boucle, 
    while loopIndex != 0:
        prefixToGet =""
        if loopIndex == 2 :
            if above :
                operator = -1
                
            else:
                loopIndex = 1
        elif loopIndex == 1:
            if behind:
                operator = 1
            
            else:
                break

        #calculate prefix
        splitedPrefixToGet[mIndex] = int(splitedPrefixToGet[mIndex]) + operator
        for entry in splitedPrefixToGet:
            prefixToGet += str(entry)
            prefixToGet += "-" #bug possibility in split, there may be a "" entry at the split!
        
        #get layer from prefix
        layerToAdd = getLayerFromPrefix(holdingGP, prefixToGet)


        if layerToAdd == "none":
            loopIndex -= 1            
        elif layerToAdd != "pass":
            relativesList.append(layerToAdd)
            

    return relativesList    


def autoMask( gP, gPLayer, maskTag = "@"): # automatically put mak on Gpencil layer depending on the name and tag
    #search for the layer prefix
    
    prefix = getPrefix(gPLayer)
    print("prefix is ", prefix)
    if prefix.find(maskTag) != -1:
        prefix = prefix.replace (maskTag,"")
        
        #search for the elder siblings without the tag
        maskList = []
        relativesList = getRelativesFromPrefix( gP, prefix,0,False,True)
        for relative in relativesList:
            if relative.info.find(maskTag) == -1:
                maskList.append(relative)
        
        #add those sibblings as mask
        print(gPLayer.info, " should be be masked by:")
        for mask in maskList:
            
            #mask true
            bpy.context.object.data.layers[gPLayer.info].use_mask_layer = True

            #get current layer index
            index=0
            for layer in gP.data.layers:
                if layer == gPLayer:
                    break
                index +=1
            #set selected
            bpy.ops.gpencil.layer_active(layer=index)
            try:
                bpy.ops.gpencil.layer_mask_add(name=mask.info)
            except RuntimeError:
                pass
            
            #add mask as mask
            print("layer",mask.info)
            pass
    else:
         print(gPLayer.info, " shall not be masked")
    
        
#Action
#curveAsGPencil( keepOriginal = False, searchForIdentifier = False  )
gP = bpy.context.scene.objects["root"]
for layerKey in gP.data.layers.keys():
    layer = gP.data.layers[layerKey]
    autoMask(gP,layer)
    
