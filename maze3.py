#https://github.com/sss140/maze_Python/blob/main/maze3.py

from enum import IntEnum
import random
import sys

import pygame
from pygame.locals import *


class Color(IntEnum):
    WALL = 0 #壁
    WAY = 1  #道
    PATH = 2 #探索用
getColor = lambda myColor:["Gray","Black","Yellow"][myColor]

class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
getDist = lambda dctn,dstc:[(-dstc,0),(dstc,0),(0,-dstc),(0,dstc)][dctn]

def getPos(myPos,dctn,dstc):
    innerDstc = getDist(dctn,dstc)
    return [myPos[0]+innerDstc[0],myPos[1]+innerDstc[1]]

#４方向のマスを検索
def get4Dctns(pos,dstc = 2,targetColor = Color.WALL):
    isInRange = lambda pos:not(pos[0] < 0 or pos[0] >= rowNum or pos[1] < 0 or pos[1] >= colNum)
    movableDctns = []
    for dctn in range(4):
        innerPos = getPos(pos,dctn,dstc)
        if isInRange(innerPos) and matrix[innerPos[0]][innerPos[1]] == targetColor:
            movableDctns.append(dctn)
    random.shuffle(movableDctns)
    return movableDctns
#移動
def movePos(pos,dctn):
    for dstc in range(1,3):
        innerPos = getPos(pos,dctn,dstc)
        setMatrix(innerPos,Color.WAY)
    return innerPos

#配列に値を入力
def setMatrix(myPos,myColor):
    matrix[myPos[0]][myPos[1]] = myColor
    sequences.append((myPos,myColor))

#迷路を作成
def makeMaze(startPoint):
    intersecs = [startPoint]
    while intersecs:
        myPos = intersecs.pop(random.randrange(len(intersecs)))
        fourDctns = get4Dctns(myPos)
        while fourDctns:
            myPos = movePos(myPos,fourDctns[0])
            intersecs.append(myPos)
            fourDctns = get4Dctns(myPos)      
    setMatrix(endPoint,Color.WAY)

#再帰関数でゴールが見つかるまで全探索
def solveMaze(pastPos):
    myPos = pastPos
    setMatrix(myPos,Color.PATH)
    dctns = get4Dctns(myPos,1,Color.WAY)
    for dctn in dctns:
        newPos = getPos(myPos,dctn,1)
        if newPos == endPoint:
            global isSolved
            isSolved = True
            setMatrix(endPoint,Color.PATH)
        if not(isSolved):
            solveMaze(newPos)
    if not(isSolved):
        setMatrix(myPos,Color.WAY)
        
def draw():
    pygame.init()
    screen = pygame.display.set_mode((colNum*10, rowNum*10))    
    pygame.display.set_caption("Maze Solver")              
    num = 0
    screen.fill(getColor(Color.WALL))  
    while(1):
        if(len(sequences)>num):
            pygame.display.set_caption(str(num) + '/' + str(len(sequences)-1))  
            myPos = sequences[num][0]
            myRect = (myPos[1]*10,myPos[0]*10,10,10)
            myColor = sequences[num][1]
            pygame.draw.rect(screen, getColor(myColor), myRect, width=0)
            pygame.display.update() 
            num += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

rowNum = 51 #行数
colNum = 51 #列数
startPoint = [-1,1] #スタート地点
endPoint = [rowNum-1,colNum-2] #ゴール地点
matrix = [[Color.WALL for _ in range(colNum)] for _ in range(rowNum)] #配列の初期化

isSolved = False
sequences = []

if __name__ == "__main__":
    makeMaze(startPoint)
    solveMaze(startPoint)
    draw()