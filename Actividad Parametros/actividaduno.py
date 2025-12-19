import cv2 as cv

image = cv.imread('Imagenes/Arbolito.jpeg',0)

cv.imshow('First Image', image)

cv.waitKey()
cv.destroyAllWindows