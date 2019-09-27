import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('frog.jpg',cv2.IMREAD_COLOR)
#img = cv2.medianBlur(img,5)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_green = np.array([110,50,100])
upper_green = np.array([110,255,255])

mask = cv2.inRange(hsv, lower_green, upper_green)

res = cv2.bitwise_and(img,img, mask=mask)

images = [hsv,mask,res]
titles = ['Image', 'Mask', 'Result']

#isolated to just one resulting image
for i in range(1):
    plt.subplot(1,1,i+1),plt.imshow(images[i])
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

cv2.imshow('image',img)
cv2.imshow('mask',mask)
cv2.imshow('result',res)
