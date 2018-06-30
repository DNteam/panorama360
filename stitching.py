import cv2
import numpy as np
import matplotlib.pyplot as plt
import homography as hm

#read images
img1 = cv2.imread('image/1.jpg',-1)  
img2 = cv2.imread('image/2.jpg',-1)
img3 = cv2.imread('image/3.jpg',-1)   
img4 = cv2.imread('image/4.jpg',-1)  
img5 = cv2.imread('image/5.jpg',-1)
img6 = cv2.imread('image/6.jpg',-1)  

img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2BGRA)
img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2BGRA)
img3 = cv2.cvtColor(img3,cv2.COLOR_BGR2BGRA)
img4 = cv2.cvtColor(img4,cv2.COLOR_BGR2BGRA)
img5 = cv2.cvtColor(img5,cv2.COLOR_BGR2BGRA)
img6 = cv2.cvtColor(img6,cv2.COLOR_BGR2BGRA)

imgList =[img4,img2,img1,img3,img6,img5]

check =[0,0,0,0,0,0]
count = [0,0,0,0,0,0]

inliers = [] 
temp=[]
index=0
while index< len(imgList)-1:
    counter=0
    for i in range(0,len(imgList)):
        if i != index:
            if hm.getInliers(imgList[index],imgList[i]) > 30:
                counter+=1
    inliers.append(counter)
    index+=1

flag=0
for i in range(0,len(inliers)):
    if inliers[i] > 2:
        flag = 1
        break

place = []
wait=[]
Max = 0
if flag == 0:
    order=[imgList[0]]
    value=[]
    for i in range(0,len(imgList)):
        value.append([])
        for j in range(0,len(imgList)):
            if i != j:
                temp = hm.getInliers(imgList[i],imgList[j])
                value[i].append(temp)
            else:
                value[i].append(0)
            
    co=0
    i=0
    while co!=1:
        Max =0
        for j in range(0,len(value[i])):
            if value[i][j]>value[i][Max]:
                Max = j
        if value[i][Max]>=50:
            order.append(imgList[Max])
            value[Max][i]=0
            value[i][Max]=0
            i=Max
        else:
            co=1

    co=0
    i=0
    while co !=1:
        Max=0
        for j in range(0,len(value[i])):
            if value[i][j]>value[i][Max]:
                Max = j
        
        if value[i][Max]>=50:
            order.insert(0,imgList[Max])
            value[Max][i]=0
            value[i][Max]=0
            i=Max
        else:
            co=1

    
    mid = len(order)/2+1 
    result=order[mid]
    index=mid -1
    while index>= 0:
        homo,ct = hm.detect(result,order[index])
        result,movedimg,xmin = hm.warpHomo(result,order[index],homo)
        h,w,c = movedimg.shape
        for i in range(0,h):
            for j in range(0,w):
                if movedimg[i,j][3] == 255:
                    result[i,j]=movedimg[i,j]
        index=index-1

    index=mid +1
    while index< len(order):
        homo,ct = hm.detect(result,order[index])
        result,movedimg,xmin = hm.warpHomo(result,order[index],homo)
        h,w,c = movedimg.shape
        for i in range(0,h):
            for j in range(0,w):
                if movedimg[i,j][3] == 255:
                    result[i,j]=movedimg[i,j]
        index=index+1
    result = cv2.cvtColor(result,cv2.COLOR_BGR2BGRA)
    writer = cv2.imwrite('image/result.png',result)
else:
    for i in range(1,len(inliers)):
        if inliers[Max] < inliers[i]:
            Max = i

    result = imgList[Max]
    check[Max]=1
    del(count[Max])
    while len(count) != 0:
        index=0
        while index < len(imgList):
            if check[index]!=1 :
                homo,ct = hm.detect(result,imgList[index])
                if ct >= 30:
                    result,movedimg,xmin = hm.warpHomo(result,imgList[index],homo)
                    h,w,c = movedimg.shape
                    for i in range(0,h):
                        for j in range(0,w):
                            if movedimg[i,j][3] == 255:
                                result[i,j]=movedimg[i,j]
                    del(count[0])
                    check[index]=1
            index=index+1


    result = cv2.cvtColor(result,cv2.COLOR_BGR2BGRA)

    writer = cv2.imwrite('image/result.png',result)


