from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
#import serial

#Serial Communication Initialization
#ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
#ser = serial.Serial ("COM13", 9600)


data = 'S'
data1 = 'A'
ctx = 0
cty = 0
cy = 0
cx = 0
a = 1
counter = 0
direction = ""


ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=32, help="max buffer size")
args = vars(ap.parse_args())

pts = deque(maxlen=args["buffer"])


if not args.get("video", False):
    vs = VideoStream(src=0).start()
else:
    vs = cv2.VideoCapture(args["video"])
time.sleep(2.0)


while True:
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame
    if frame is None:
        break

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    ballLower = np.array([0, 0, 200], dtype=np.uint8)
    ballUpper = np.array([200, 40, 255], dtype=np.uint8)


    mask = cv2.inRange(hsv, ballLower, ballUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        cty = cy
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
            else:
                cx = cx
                cy = cy
            if (cty != 0 and (cy - cty) > 10):
                a = cx
                cx = ctx
            else:
                a = 0

        # Membuat Garis Center
        cv2.line(frame, (cx, 0), (cx, 720), (255, 0, 0), 1)
        cv2.line(frame, (0, cy), (1280, cy), (255, 0, 0), 1)
        #cv2.drawContours(frame, cnts, -1, (0, 255, 0), 1)

    pts.appendleft(center)

    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
        if counter >= 10 and i == 1 and pts[-10] is not None:
            cx = pts[-10][0] - pts[i][0]
            cy = pts[-10][1] - pts[i][1]
            (ctx, cty) = ("", "")


            if np.abs(cx) > 20:
                dirX = "East" if np.sign(cx) == 1 else "West"

            if np.abs(cy) > 20:
                dirY = "North" if np.sign(cy) == 1 else "South"

            if ctx != "" and cty != "":
                direction = "{}-{}".format(ctx, cty)

            else:
                direction = ctx if ctx != "" else cty

        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (0, 0, 255), 3)
    cv2.putText(frame, "dx: {}, dy: {}".format(cx, cy),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)

    cv2.imshow("Frame", frame)
    counter += 1
    k = cv2.waitKey(40)
    if k == 27:
        break

if not args.get("video", False):
    vs.stop()
else:
    vs.release()

cv2.destroyAllWindows()


