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

imgList =[img4,img2,img1,img3]

# imgList =[img1,img2,img3]

inliers = [] 
temp=[]
index=0
while index< len(imgList)-1:
    counter=0
    for i in range(0,len(imgList)):
        if i != index:
            if hm.getInliers(imgList[index],imgList[i]) > 20:
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
    imgSaver = imgList[0]
    place.append(0)
    i=1
    while i<len(imgList):
        homo, threshold = hm.detect(imgSaver,imgList[i])
        if threshold <=20:
            wait.append(imgList[i])
            i+=1
            continue
        result,movedimg,xmin = hm.warpHomo(imgSaver,imgList[i],homo)

        if xmin < 0:
            place.insert(0,i)
        else:
            place.append(i)
        
        h,w,c = movedimg.shape
        for j in range(0,h):
            for k in range(0,w):
                if movedimg[j,k][3] == 255:
                    result[j,k]=movedimg[j,k]
        i+=1
    
    while len(wait) != 0:
        i=0
        while i< len(wait):
            homo, threshold = hm.detect(imgSaver,wait[i])
            if threshold >20:
                result,movedimg,xmin = hm.warpHomo(imgSaver,wait[i],homo)

                if xmin < 0:
                    place.insert(0,i)
                else:
                    place.append(i) 
                
                h,w,c = movedimg.shape
                for j in range(0,h):
                    for k in range(0,w):
                        if movedimg[j,k][3] == 255:
                            result[j,k]=movedimg[j,k]
                del(wait[i])
                continue
            i+=1    
    Max = place[len(place)/2]
else:
    for i in range(1,len(inliers)):
        if inliers[Max] < inliers[i]:
            Max = i


mid= Max
result = imgList[mid]
index= len(place)/2-1
while index >= 0:
    homo,ct = hm.detect(result,imgList[place[index]])
    result,movedimg,xmin = hm.warpHomo(result,imgList[place[index]],homo)
    h,w,c = movedimg.shape
    for i in range(0,h):
        for j in range(0,w):
            if movedimg[i,j][3] == 255:
                result[i,j]=movedimg[i,j]
    index=index-1


mid=Max
index=len(place)/2+1

while index< len(place):
    homo,ct = hm.detect(result,imgList[place[index]])
    result,movedimg,xmin = hm.warpHomo(result,imgList[place[index]],homo)
    h,w,c = movedimg.shape
    for i in range(0,h):
        for j in range(0,w):
            if movedimg[i,j][3] == 255:
                result[i,j]=movedimg[i,j]
    index=index+1

result = cv2.cvtColor(result,cv2.COLOR_BGR2BGRA)

writer = cv2.imwrite('image/result3.png',result)


