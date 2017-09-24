
import maya.cmds as cmds
import math
import functools

def createUI(pWindowTitle, pApplyCallback):
    windowID = 'WindowID'
    
    if cmds.window(windowID, exists = True):
        cmds.deleteUI(windowID)
        
    cmds.window(windowID, title = pWindowTitle, sizeable = False, resizeToFitChildren = True)
    cmds.rowColumnLayout(numberOfColumns = 2, columnWidth = [(1, 190), (2,60)], columnOffset=[(1, 'right', 3)])
    cmds.text(label = 'Stair Case Height: ')
    height = cmds.intField(value = 10)
    cmds.text(label = 'Width of Staircase: ')
    width = cmds.intField(value = 5)
    cmds.text(label = 'Steepness(normal, steep, or shallow): ')
    steepness = cmds.textField(text = 'normal')  
    
    cmds.separator(h = 10, style = 'none')
    cmds.separator(h = 10, style = 'none')
    
    cmds.button(label = 'Apply', command = functools.partial(pApplyCallback, height, width, steepness))
    
    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists = True):
            cmds.deleteUI(windowID)
            
    cmds.button(label='Cancel', command = cancelCallback)
    
    cmds.showWindow()
    
def generateStairs(height, width, steepness):       
    braceHeight = 10
    braceWidth = 1
    braceDepth = .5
    caseWidth = width+0.0
    caseHeight = height+0.0
    totalStairs = height+0.0
    base = 0.0
    s1 = str(steepness)
    
    if steepness == "steep":
        base = caseHeight/2 
        
    if steepness == "normal":
        base = caseHeight
        
    if steepness == "shallow":
        base = caseHeight*2

    a2 = base *base
    b2 = caseHeight * caseHeight
    braceHeight = (a2 + b2)**(.5)

    result = cmds.polyCube(w=braceWidth, h=braceHeight, d=braceDepth, cuv = 4, name='brace#')
    cmds.move(0, 0, -caseWidth/2.0, result)
    braceName = result[0]
    result2 = cmds.polyCube(w=braceWidth, h=braceHeight, d=braceDepth, cuv = 4, name = 'brace#')
    cmds.move(0, 0, caseWidth/2.0, result2)

    x = caseHeight/braceHeight
    rAngle = math.asin(x)
    dAngle = rAngle*57.2957795
    finalAngle = 90 - dAngle

    cmds.rotate(0, 0, finalAngle, result)
    cmds.rotate(0, 0, finalAngle, result2)

    step = cmds.polyCube(w = braceHeight/totalStairs, h = .5, depth = caseWidth, cuv = 4, name='step#')
    stepName = step[0]
    
    if steepness == "normal":
    
        for i in range(1, int(totalStairs/2)):
            newStep = cmds.polyCube(w = braceHeight/totalStairs, h = .5, depth = caseWidth, cuv = 4, name='step#')
            y = (caseHeight/base)*(i)
            x = -i
            cmds.move(x, y, 0, newStep)
   
    
        for i in range(1, int(totalStairs/2)):
            newStep = cmds.polyCube(w = braceHeight/totalStairs, h = .5, depth = caseWidth, cuv = 4, name='step#')
            y = (caseHeight/base)*(-i)
            x = i
            cmds.move(x, y, 0, newStep)

    if steepness == "steep":
    
        for i in range(1, int(totalStairs/2)):
            newStep = cmds.polyCube(w = braceHeight/totalStairs, h = .5, depth = caseWidth, cuv = 4, name='tStep#')
            y = ((caseHeight/base)*(i))/2.0
            x = -i/2.0
            cmds.move(x, y, 0, newStep)
   

        for i in range(1, int(totalStairs/2)):
            newStep = cmds.polyCube(w = braceHeight/totalStairs, h = .5, depth = caseWidth, cuv = 4, name='bStep#')
            y = ((caseHeight/base)*(-i))/2.0
            x = i/2.0
            cmds.move(x, y, 0, newStep)

    if steepness == "shallow":

        for i in range(1, int(totalStairs/2)):
            newStep = cmds.polyCube(w = braceHeight/totalStairs, h = .5, depth = caseWidth, cuv = 4, name='tStep#')
            y = ((caseHeight/base)*(i))*2.0
            x = -i*2.0
            cmds.move(x, y, 0, newStep)
   

        for i in range(1, int(totalStairs/2)):
            newStep = cmds.polyCube(w = braceHeight/totalStairs, h = .5, depth = caseWidth, cuv = 4, name='bStep#')
            y = ((caseHeight/base)*(-i))*2.0
            x = i*2.0
            cmds.move(x, y, 0, newStep)  
            
    stepList = cmds.ls('brace*', 'step*', 'tStep*', 'bStep*', type = 'mesh')  
    cmds.select(stepList) 
    print stepList
    cmds.polyUnite(stepList)         
              
def applyCallback(height, width, steepness, *pArgs):
    h = cmds.intField(height, query = True, value = True)
    w = cmds.intField(width, query = True, value = True)
    steep = cmds.textField(steepness, query = True, text = True)
    
    generateStairs(h, w, steep)
    
createUI('Staircase Generator', applyCallback)

