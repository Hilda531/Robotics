import cv2
import numpy as np

def nothing(x):
    pass

vid = cv2.VideoCapture(0)

cv2.namedWindow("DET")
cv2.createTrackbar("LH", "DET", 0, 255, nothing)
cv2.createTrackbar("LS", "DET", 0, 255, nothing)
cv2.createTrackbar("LV", "DET", 0, 255, nothing)
cv2.createTrackbar("UH", "DET", 255, 255, nothing)
cv2.createTrackbar("US", "DET", 255, 255, nothing)
cv2.createTrackbar("UV", "DET", 255, 255, nothing)

while True:
    _, frame = vid.read()

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

    #rect = np.ones((5, 5), np.uint8)

    #mask = cv2.erode(mask, rect)

    # contour detection
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        apx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        if area > 400:
            cv2.drawContours(frame, [apx], 0, (0, 0, 0), 3)
            x = apx.ravel()[0]
            y = apx.ravel()[1]

            if len(apx) < 5:
                cv2.putText(frame, "Rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                print('rectangle')

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)

    esc = cv2.waitKey (1)
    if esc == 27:
        break
vid.release()
cv2.destroyAllWindows()