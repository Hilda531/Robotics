import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    # Convert to HSV
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Make Yellow Color Range
    lower_yellow = np.array([32, 95, 120], dtype="uint8")
    upper_yellow = np.array([44, 255, 255], dtype="uint8")

    # Make Yellow Mask
    mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

    rect = np.ones((5, 5), np.uint8)

    mask = cv2.erode(mask_yellow, rect)

    #contour detection
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        apx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)

        if area > 400:
            cv2.drawContours(frame, [apx], 0, (0, 0, 0), 3)
            x = apx.ravel()[0]
            y = apx.ravel()[1]

            if len(apx) == 4:
                cv2.putText(frame, "Rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                print('rectangle')



    cv2. imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()