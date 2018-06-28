import cv2
import numpy as np
MIN = 10

def detect(imgUnchange, imgchange):
    #use Sift to find feature point
    sift = cv2.xfeatures2d.SURF_create()
    keyPoint1, destination1 = sift.detectAndCompute(imgUnchange,None)
    keyPoint2, destination2 = sift.detectAndCompute(imgchange,None)

    # find the two similar feature with brute force matcher
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(destination1,destination2,k=2)

    #threshold
    good = []
    for m,n in matches:
        if m.distance < .75*n.distance:
            good.append(m)

    #find homography and inliers
    if len(good)>MIN:
        # get all feature point from image 1
        source_points = np.float32([ keyPoint1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        # get all feature point from image 1
        destination_points = np.float32([ keyPoint2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        #get homography matrix and all information of these matches(do all steps of RANSAC)
        HomographyMatrix, mask = cv2.findHomography(destination_points,source_points, cv2.RANSAC,5.0)
        #matchesMask is a list, it's elements have just 2 value. value 1 means it's a inlier, 2 mean it's a outlier
        matchesMask = mask.ravel().tolist() #inlier
    else:
        print "Not enough matches are found - %d/%d" % (len(good),MIN)
        matchesMask = None
    return HomographyMatrix

def warpHomo(img1, img2, HomographyMatrix):
    row,col,z = img1.shape
    h,w,c = img2.shape
    points=np.array([[[ 0.0, h]],
                    [[ 0.0, 0.0]], 
                    [[ w, 0.0 ]],
                    [[ w, h]]
    ])
    wrapped_points = cv2.perspectiveTransform(points,HomographyMatrix)

    xmin = min(wrapped_points[0][0][0],wrapped_points[1][0][0],wrapped_points[2][0][0],wrapped_points[3][0][0])
    xmax = max(wrapped_points[0][0][0],wrapped_points[1][0][0],wrapped_points[2][0][0],wrapped_points[3][0][0])
    ymin = min(wrapped_points[0][0][1],wrapped_points[1][0][1],wrapped_points[2][0][1],wrapped_points[3][0][1])
    ymax = max(wrapped_points[0][0][1],wrapped_points[1][0][1],wrapped_points[2][0][1],wrapped_points[3][0][1])

    xnew = xmax - xmin
    ynew = ymax - ymin

    xchange = 0
    ychange = 0
    if xmin < 0:
        xchange = -1 * xmin
    if ymin < 0:
        ychange = -1 * ymin

    M = np.float32([[1,0,xchange],[0,1,ychange]])
    movedimg1 = cv2.warpAffine(img1,M,(col + int(xchange), row + int(ychange)))
    movedimg2 = cv2.warpAffine(img2,M,(w + int(xchange), h + int(ychange)))

    width = 0
    height = 0

    if xnew < xmax:
        xnew = xmax
    
    if ynew < ymax:
        ynew = ymax

    if xnew > col + xchange:
        width = int(round(xnew))
    else:
        width = int(round(col+xchange))

    
    if ynew > row + ychange:
        height = int(round(ynew))
    else:
        height = int(round(row+ychange))

    homo = detect(movedimg1,movedimg2)

    result = cv2.warpPerspective(movedimg2, homo,(width, height))
    return result


img1 = cv2.imread('image/1.jpg',-1)  
img2 = cv2.imread('image/2.jpg',-1)

img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2BGRA)
img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2BGRA)

sift = cv2.xfeatures2d.SURF_create()
keyPoint1, destination1 = sift.detectAndCompute(img1,None)
keyPoint2, destination2 = sift.detectAndCompute(img2,None)

# find the two similar feature with brute force matcher
bf = cv2.BFMatcher()
matches = bf.knnMatch(destination1,destination2,k=2)

#threshold
good = []
for m,n in matches:
    if m.distance < .75*n.distance:
        good.append(m)

#find homography and inliers
if len(good)>MIN:
    # get all feature point from image 1
    source_points = np.float32([ keyPoint1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    # get all feature point from image 1
    destination_points = np.float32([ keyPoint2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    #get homography matrix and all information of these matches(do all steps of RANSAC)
    HomographyMatrix, mask = cv2.findHomography(destination_points,source_points, cv2.RANSAC,5.0)
    #matchesMask is a list, it's elements have just 2 value. value 1 means it's a inlier, 2 mean it's a outlier
    matchesMask = mask.ravel().tolist() #inlier
else:
    print "Not enough matches are found - %d/%d" % (len(good),MIN)
    matchesMask = None

result = warpHomo(img1, img2, HomographyMatrix)

cv2.imwrite("thing1.jpg",result)
cv2.imwrite("thing1.png",result)