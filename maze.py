from PIL import Image, ImageDraw
from enum import IntEnum
import random
#Y->0 X->1
#True -> wall False -> path

class Color(IntEnum):
    _WALL = 0
    _WAY = 1
    _PATH = 2

def getColor(myColor):
    if myColor == Color._WALL:
        return "Blue"
    elif myColor == Color._WAY:
        return "White"
    elif myColor == Color._PATH:
        return "Red"

class Direction(IntEnum):
    _UP = 0
    _DOWN = 1
    _LEFT = 2
    _RIGHT = 3

def getDist(dctn,dstc):
    if dctn == Direction._UP:
        return (-dstc,0)
    elif dctn == Direction._DOWN:
        return (dstc,0)
    elif dctn == Direction._LEFT:
        return (0,-dstc)
    elif dctn == Direction._RIGHT:
        return (0,dstc)

def get4Dctns(pos,dstc,targetColor):
    movableDctns = []
    for i in range(4):
        innerDstc = getDist(i,dstc)
        innerPos = [pos[0]+innerDstc[0],pos[1]+innerDstc[1]]
        if not(innerPos[0] < 0 or innerPos[0] >= rowNum or innerPos[1] < 0 or innerPos[1] >= colNum):
            if matrix[innerPos[0]][innerPos[1]] == targetColor:
                movableDctns.append(i)
    random.shuffle(movableDctns)
    return movableDctns

def movePos(pos,dctn):
    innerPos = []
    for i in range(2):
        innerDstc = getDist(dctn,i+1)
        innerPos = [pos[0]+innerDstc[0],pos[1]+innerDstc[1]]
        matrix[innerPos[0]][innerPos[1]] = Color._WAY
    return innerPos

def makeMaze():
    intersecs = [[-1,1]]
    while len(intersecs):
        random.shuffle(intersecs)
        myPos = intersecs[0]
        intersecs.pop(0)
        fourDctns = get4Dctns(myPos,2,Color._WALL)
        while len(fourDctns):
            myPos = movePos(myPos,fourDctns[0])
            fourDctns = get4Dctns(myPos,2,Color._WALL)
            intersecs.append(myPos)
    matrix[rowNum-1][colNum-2] = Color._WAY

def solveMaze(myPos):
    matrix[myPos[0]][myPos[1]] = Color._PATH
    dctns = get4Dctns(myPos,1,Color._WAY)
    for d in dctns:
        myDist = getDist(d,1)
        newPos = [myPos[0]+myDist[0],myPos[1]+myDist[1]]
        if newPos == [rowNum-1,colNum-2]:
            matrix[rowNum-1][colNum-2] = Color._PATH
            global solvedMaze
            solvedMaze = True
        if not(solvedMaze):
            solveMaze(newPos)
    if not(solvedMaze):
        matrix[myPos[0]][myPos[1]] = Color._WAY
        


def makeImage():
    img = Image.new("RGB", (colNum*oLen, rowNum*oLen), "White")
    draw = ImageDraw.Draw(img)
    for y,line in enumerate(matrix):
        for x,dot in enumerate(line):
            draw.rectangle([(x*oLen,y*oLen),(x*oLen+oLen-1,y*oLen+oLen-1)],fill=getColor(dot))
    img.show()




solvedMaze = False
rowNum = 51 #行数
colNum = 51 #列数
oLen = 15
matrix = [[Color._WALL for i in range(colNum)] for j in range(rowNum)]
makeMaze()
solveMaze([0,1])

makeImage()