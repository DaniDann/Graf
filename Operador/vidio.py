import cv2 as cv

cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()
    if ret:
        cv.imshow("video", img)
        r, g, b = cv.split(img)
        ret == 255-img
        # cv.imshow("r", r)
        # cv.imshow("g", g)
        # cv.imshow("b", b)
        img3 = cv.merge([g, b, r])
        cv.imshow("res", ret)
        cv.imshow("img3", img3)
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break
    else:
        break

cap.release()
cv.destroyAllWindows()