#!/usr/bin/env python
# coding: utf-8
#lat.txt, lon.txt(위도, 경도가 1024x1024로 저장된 파일)를 같은 폴더에 넣고 천리안 위성 영상의 위치를 찾고자 하는
#지점의 (위도,경도)를 입력하면 (행, 열)을 반환함.
import math
import numpy as np
lat = np.loadtxt('lat.txt')
lon = np.loadtxt('lon.txt')

def toGrid(x,y):
    X =-2.17351788650566e-08*x*x+3.64502730819741e-08*y*y-1.12902127612504*x*y    +143.193770067438*x+93.6424539767530*y-11365.1728109130
    Y = 0.277852347859833*x*x -0.433381482384967*y*y-9.07937755577695e-08*x*y    -85.0999884251540*x+109.931550342823*y-3662.91295349115
    X1 = round(X)
    Y1 = round(Y)
    print(X1,Y1)
    cnt = 0
    X1 = int(X1)
    Y1 = int(Y1)
    if X1<0:
        X1 = 0
    if Y1<0:
        Y1 = 0

    while cnt<100:
        tx = lat[X1,Y1]
        ty = lon[X1,Y1]
       ## print("tx, ty: ", tx,ty)
        mind = abs(tx-x)+abs(ty-y)
        X2 = X1
        Y2 = Y1
        for i in range(-1,2):
            for j in range(-1,2):
           ##     print("abs(lat[X1+i,Y1]-x)+abs(lon[X1,Y1+j]-y) : ",abs(lat[X1+i,Y1+j]-x)+abs(lon[X1+i,Y1+j]-y))
                if abs(lat[X1+i,Y1+j]-x)+abs(lon[X1+i,Y1+j]-y)<mind:
                    X2 = X1+i
                    Y2 = Y1+j
                    mind = abs(lat[X1+i,Y1+j]-x)+abs(lon[X1+i,Y1+j]-y)
                   # print("!!!!!!!!!!!!!!!1: ", cnt, mind)
                    
        if X1==X2 and Y1 == Y2:
            break
        else:
            X1 = X2
            Y1 = Y2
            cnt= cnt+1
   # print(cnt)
    return Y1, X1
