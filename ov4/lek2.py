import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('british_short.jpg',0)
retval, threshold = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

# Otsu's thresholding
blur = cv2.GaussianBlur(img,(15,15),0)
ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


cv2.imshow('original',img)
cv2.imshow('threshold',threshold)
cv2.imshow('threshold2',th2)
cv2.waitKey(0)
cv2.destroyAllWindows()