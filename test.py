import cv2
import homography as hm

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
order=[0]
value=[]
for i in range(0,len(imgList)):
    value.append([])
    for j in range(0,len(imgList)):
        if i != j:
            temp = hm.getInliers(imgList[i],imgList[j])
            value[i].append(temp)
        else:
            value[i].append(0)
        

print value


flag=0
i=0
while flag!=1:
    Max =0
    for j in range(0,len(value[i])):
        if value[i][j]>value[i][Max]:
            Max = j
    if value[i][Max]>=50:
        print value[i][Max]
        order.append(Max)
        value[Max][i]=0
        value[i][Max]=0
        i=Max
    else:
        flag=1

print value
flag=0
i=0
while flag !=1:
    Max=0
    for j in range(0,len(value[i])):
        if value[i][j]>value[i][Max]:
            Max = j
    
    if value[i][Max]>=50:
        order.insert(0,Max)
        value[Max][i]=0
        value[i][Max]=0
        i=Max
    else:
        flag=1

print order
    
# mid = 2
# result=imgList[mid]
# index=mid -1
# while index>= 0:
#     homo,ct = hm.detect(result,imgList[index])
#     result,movedimg,xmin = hm.warpHomo(result,imgList[index],homo)
#     h,w,c = movedimg.shape
#     for i in range(0,h):
#         for j in range(0,w):
#             if movedimg[i,j][3] == 255:
#                 result[i,j]=movedimg[i,j]
#     index=index-1

# index=mid +1
# while index< len(imgList):
#     homo,ct = hm.detect(result,imgList[index])
#     result,movedimg,xmin = hm.warpHomo(result,imgList[index],homo)
#     h,w,c = movedimg.shape
#     for i in range(0,h):
#         for j in range(0,w):
#             if movedimg[i,j][3] == 255:
#                 result[i,j]=movedimg[i,j]
#     index=index+1
# result = cv2.cvtColor(result,cv2.COLOR_BGR2BGRA)
# writer = cv2.imwrite('image/result1.png',result)



