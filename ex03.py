import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

path1 = 'mario.jpg'
path2 = 'goldCoin.png'
if os.path.isfile(path1)&os.path.isfile(path2):
	img_rgb = cv2.imread(path1)
	template = cv2.imread(path2, 0)
else:
    print ("The file " + path1 + " does not exist.")
	
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite('res.png',img_rgb)
