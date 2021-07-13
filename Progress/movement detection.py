import cv2
import numpy as np

vid = cv2.VideoCapture('vtest.avi')
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('detect.mp4v', fourcc, 20.0, (768, 576))
#print(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
#print(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

ret, frame1 = vid.read()
ret, frame2 = vid.read()

while vid.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame1, contours, -1, (255, 0, 0), 1)
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 700:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (50, 70, 150), 3)

    cv2.imshow("inter", frame1)
    #out.write(frame1)
    frame1 = frame2
    ret, frame2 = vid.read()
    k = cv2.waitKey(40)
    if k == 27:
        break

cv2.destroyAllWindows()
vid.release()
#out.release()