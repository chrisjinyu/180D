import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

path1 = 'Sephiroth.png'
if os.path.isfile(path1):
    img = cv2.imread(path1, 0)
else:
    print ("The file " + path1 + " does not exist.")
	
edges = cv2.Canny(img,190,300)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()