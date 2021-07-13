import cv2
import numpy as np

def nothing(x):
    pass

cv2.namedWindow("DET")
cv2.createTrackbar("LH", "DET", 0, 255, nothing)
cv2.createTrackbar("LS", "DET", 0, 255, nothing)
cv2.createTrackbar("LV", "DET", 0, 255, nothing)
cv2.createTrackbar("UH", "DET", 255, 255, nothing)
cv2.createTrackbar("US", "DET", 255, 255, nothing)
cv2.createTrackbar("UV", "DET", 255, 255, nothing)

while True:
    frame = cv2.imread('smarties.png')

    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lh = cv2.getTrackbarPos("LH", "DET")
    ls = cv2.getTrackbarPos("LS", "DET")
    lv = cv2.getTrackbarPos("LV", "DET")

    uh = cv2.getTrackbarPos("UH", "DET")
    us = cv2.getTrackbarPos("US", "DET")
    uv = cv2.getTrackbarPos("UV", "DET")

    LB = np.array([lh, ls, lv])
    UB = np.array([uh, us, uv])

    mask = cv2.inRange(HSV, LB, UB)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)

    esc = cv2.waitKey (1)
    if esc == 27:
        break

cv2.destroyAllWindows()