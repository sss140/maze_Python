

from enum import IntEnum
import random
import pygame
from pygame.locals import *
import sys

class Color(IntEnum):
    WALL = 0 #壁
    WAY = 1 #道
    PATH = 2 #探索用
def getColor(myColor):
    if myColor == Color.WALL:
        return "Purple"
    elif myColor == Color.WAY:
        return "White"
    elif myColor == Color.PATH:
        return "Red"

class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
def getDist(dctn,dstc):
    if dctn == Direction.UP:
        return (-dstc,0)
    elif dctn == Direction.DOWN:
        return (dstc,0)
    elif dctn == Direction.LEFT:
        return (0,-dstc)
    elif dctn == Direction.RIGHT:
        return (0,dstc)

#４方向のマスを検索
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
#移動
def movePos(pos,dctn):
    for i in range(2):
        innerDstc = getDist(dctn,i+1)
        innerPos = [pos[0]+innerDstc[0],pos[1]+innerDstc[1]]
        setMatrix(innerPos,Color.WAY)
    return innerPos

#配列に値を入力
def setMatrix(myPos,myColor):
    matrix[myPos[0]][myPos[1]] = myColor
    seq.append((myPos,myColor))

＃迷路を作成
def makeMaze():
    intersecs = [[-1,1]]
    while len(intersecs):
        random.shuffle(intersecs)
        myPos = intersecs[0]
        intersecs.pop(0)
        fourDctns = get4Dctns(myPos,2,Color.WALL)
        while len(fourDctns):
            myPos = movePos(myPos,fourDctns[0])
            intersecs.append(myPos)
            fourDctns = get4Dctns(myPos,2,Color.WALL)
            
    setMatrix([rowNum-1,colNum-2],Color.WAY)

#再帰関数でゴールが見つかるまで全探索
def solveMaze(myPos):
    setMatrix(myPos,Color.PATH)
    for d in get4Dctns(myPos,1,Color.WAY):
        myDist = getDist(d,1)
        newPos = [myPos[0]+myDist[0],myPos[1]+myDist[1]]
        if newPos == [rowNum-1,colNum-2]:
            global solved
            solved = True
            setMatrix([rowNum-1,colNum-2],Color.PATH)
        if not(solved):
            solveMaze(newPos)
    if not(solved):
        setMatrix(myPos,Color.WAY)
        
def draw():
    pygame.init()
    screen = pygame.display.set_mode((colNum*10, rowNum*10))    
    pygame.display.set_caption("Maze Solver")              
    num = 0
    screen.fill(getColor(Color.WALL))  
    while(1):
        if(len(seq)>num):
            myPos = seq[num][0]
            myRect = (myPos[1]*10,myPos[0]*10,10,10)
            myColor = seq[num][1]
            pygame.draw.rect(screen, getColor(myColor), myRect, width=0)
            pygame.display.update() 
            num += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


rowNum = 101 #行数
colNum = 51 #列数
matrix = [[Color.WALL for i in range(colNum)] for j in range(rowNum)]
solved = False
seq = []

makeMaze()
solveMaze([0,1])
draw()