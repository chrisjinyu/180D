import cv2
import numpy as np

cap = cv2.VideoCapture(0)

_, frame = cap.read()

cv2.imwrite("pic.jpg", frame)