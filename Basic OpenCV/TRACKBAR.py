import numpy as np
import cv2 as cv

def nothing(x):
    print(x)

gbr = np.zeros((400, 400, 3), np.uint8)
cv.namedWindow('gambar')

cv.createTrackbar('B', 'gambar', 0, 255, nothing)
cv.createTrackbar('G', 'gambar', 0, 255, nothing)
cv.createTrackbar('R', 'gambar', 0, 255, nothing)

while(1):
    cv.imshow('gambar', gbr)
    t = cv.waitKey(1) & 0xFF
    if t == ord('r'):
        break
    b = cv.getTrackbarPos('B', 'gambar')
    g = cv.getTrackbarPos('G', 'gambar')
    r = cv.getTrackbarPos('R', 'gambar')

    gbr[:] = [b, g, r]

cv.destroyAllWindows()