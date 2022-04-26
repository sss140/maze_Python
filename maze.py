from PIL import Image, ImageDraw
from enum import IntEnum
import random
#Y->0 X->1
#True -> wall False -> path
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

def get4Dctns(pos,dstc):
    movableDctns = []
    for i in range(4):
        innerDstc = getDist(i,dstc)
        innerPos = [pos[0]+innerDstc[0],pos[1]+innerDstc[1]]
        if not(innerPos[0] < 0 or innerPos[0] >= rowNum or innerPos[1] < 0 or innerPos[1] >= colNum):
            if matrix[innerPos[0]][innerPos[1]]:
                movableDctns.append(i)
    random.shuffle(movableDctns)
    return movableDctns

def movePos(pos,dctn):
    innerPos = []
    for i in range(2):
        innerDstc = getDist(dctn,i+1)
        innerPos = [pos[0]+innerDstc[0],pos[1]+innerDstc[1]]
        matrix[innerPos[0]][innerPos[1]] = False
    return innerPos

def makeMaze():
    intersecs = [[-1,1]]
    while len(intersecs):
        random.shuffle(intersecs)
        myPos = intersecs[0]
        intersecs.pop(0)
        fourDctns = get4Dctns(myPos,2)
        while len(fourDctns)>0:
            myPos = movePos(myPos,fourDctns[0])
            fourDctns = get4Dctns(myPos,2)
            intersecs.append(myPos)
    matrix[rowNum-1][colNum-2] = False

def makeImage():
    img = Image.new("RGB", (colNum*10, rowNum*10), "White")
    draw = ImageDraw.Draw(img)
    for y,line in enumerate(matrix):
        for x,dot in enumerate(line):
            if dot:
                draw.rectangle([(x*10,y*10),(x*10+9,y*10+9)],fill="Blue")
    img.show()



rowNum = 201 #行数
colNum = 201 #列数
matrix = [[True for i in range(colNum)] for j in range(rowNum)]
makeMaze()
makeImage()