import cv2 as cv
import numpy as np

img = cv.imread('Imagenes/Arbolito.jpeg', 1)
img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Imagenes/Arbolito.jpeg', img2)

x, y = img2.shape[:2]
print(x, y)

for i in range(x):
    for j in range(y):
        img2[i, j] = 255 - img2[i, j]

cv.imshow('img2b', img2)

img3 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img4 = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
img5 = cv.cvtColor(img, cv.COLOR_BGR2HSV)

cv.imshow('img', img)
cv.imshow('img2', img2)
cv.imshow('img3', img3)
cv.imshow('img4', img4)
cv.imshow('img5', img5)

cv.waitKey(0)
cv.destroyAllWindows()