# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 02:40:05 2020
USED FOR TESTING #CONNECTIONS/TIME FOR DIFFERENT BROWSER HEIGHTS
@author: hasimsait
"""
from matplotlib.pyplot import *
import numpy as np

def readtxt(thefilepath):
    connList=[]
    timeList=[]
    count = len(open(thefilepath).readlines())
    f = open(thefilepath, "r")
    for i in range(int(count/3)):
        f.readline()
        numberOfConn=int(f.readline()[:-1])
        timeItTook=float(f.readline()[:-1])
        connList.append(numberOfConn)
        timeList.append(timeItTook)
    #connList=[Xc,Yc,Zc...]
    #timeList=[Xt,Yt,Zt...]
    mylist=[connList,timeList]
    f.close()
    m, b = np.polyfit(mylist[0], mylist[1], 1)
    print(str(m)+"*connections+"+str(b)+"seconds with "+thefilepath)
    matplotlib.pyplot.scatter(connList, timeList)
    return mylist

slope2160=readtxt("2160_time.txt")#may be unstable, test on some large acc
slope1080=readtxt("1080_time.txt")#2160 performs better
slope2160_2=readtxt("2160_time_initial2.txt")
print(slope2160)
print(slope1080)