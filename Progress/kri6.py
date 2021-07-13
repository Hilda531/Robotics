import cv2
import numpy as np
#import serial ***
from time import sleep
import time

#oii ser = serial.Serial("/dev/OpenCM9.04", 9600)  # Open port with baud rate
# data = 0
def B():
    cap = cv2.VideoCapture(0)
    # Set camera resolution
    cap.set(3, 480)  # 3,480
    cap.set(4, 320)  # 4,320
    _, frame = cap.read()
    rows, cols, _ = frame.shape

    y_medium = int(rows / 2)
    x_medium = int(cols / 2)
    #center = int(cols / 2)
    #position = 90  # degrees

    while True:
        _, frame = cap.read()
        cv2.rectangle(frame, (210, 0), (430, 360), (0, 0, 255), 1)

        # Convert to grayscale
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Convert to HSV
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Make Yellow Color Range
        lower_led = np.array([32, 95, 120], dtype="uint8")
        upper_led = np.array([44, 255, 255], dtype="uint8")

        # Make Yellow Mask
        mask_yellow = cv2.inRange(img_hsv, lower_led, upper_led)

        # Make White Mask
        #mask_white = cv2.inRange(gray, 200, 255)

        # Make Mask of White or Yellow
        #mask_yw = cv2.bitwise_or(mask_white, mask_yellow)

        # Make Mask of Gray and (White or Yellow)
        #mask_yw_image = cv2.bitwise_and(gray, mask_yw)

        # Gaussian blur
        blur = cv2.GaussianBlur(mask_yellow, (5, 5), 0)

        # Color thresholding
        ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)

        # For delete noise
        # The erosion makes the object in white smaller.
        thresh = cv2.erode(thresh, None, iterations=2)
        # The dilatation makes the object in white bigger.
        thresh = cv2.dilate(thresh, None, iterations=5)

        contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)[-2:]
        #contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)

            y_medium = int((y + y + h) / 2)
            x_medium = int((x + x + w) / 2)
            break

        cv2.line(frame, (x_medium, 0), (x_medium, 360), (255, 0, 0), 1)
        cv2.line(frame, (0, y_medium), (640, y_medium), (255, 0, 0), 1)
        #cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)

        if x_medium < 430 and x_medium > 210:
            print("On Track!")
            data = 'W'
        else:
            print("I don't see the line")
            break

        cv2.imshow("Frame", frame)
        cv2.imshow("contours", thresh)

        cv2.waitKey(1) & 0xFF

def A():
    data = 'S'
    data1 = 'A'

    cap = cv2.VideoCapture(0)
    # Set camera resolution
    cap.set(3, 480)  # 3,480
    cap.set(4, 320)  # 4,320
    _, frame = cap.read()
    rows, cols, _ = frame.shape

    y_medium = int(rows / 2)
    x_medium = int(cols / 2)
    center = int(cols / 2)
    position = 90  # degrees

    while True:
        _, frame = cap.read()
        #cv2.rectangle(frame, (210, 0), (430, 359), (0, 0, 255), 1)

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Convert to HSV
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Make Yellow Color Range
        lower_led = np.array([32, 95, 120], dtype="uint8")
        upper_led = np.array([44, 255, 255], dtype="uint8")

        # Make Yellow Mask
        mask_yellow = cv2.inRange(img_hsv, lower_led, upper_led)

        # Make White Mask
        #mask_white = cv2.inRange(gray, 200, 255)

        # Make Mask of White or Yellow
        #mask_yw = cv2.bitwise_or(mask_white, mask_yellow)

        # Make Mask of Gray and (White or Yellow)
        #mask_yw_image = cv2.bitwise_and(gray, mask_yw)

        # Gaussian blur
        blur = cv2.GaussianBlur(mask_yellow, (5, 5), 0)

        # Color thresholding
        ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)

        # For delete noise
        # The erosion makes the object in white smaller.
        thresh = cv2.erode(thresh, None, iterations=2)
        # The dilatation makes the object in white bigger.
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)[-2:]
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)

            y_medium = int((y + y + h) / 2)
            x_medium = int((x + x + w) / 2)
            break

        cv2.line(frame, (x_medium, 0), (x_medium, 360), (255, 0, 0), 1)
        cv2.line(frame, (0, y_medium), (640, y_medium), (255, 0, 0), 1)

        # Move servo motor

        if x_medium < center - 40:
            position += 2
        if x_medium > center + 40:
            position -= 2

        print(x_medium, position)

        if position > 180:
            position = 180
        if position < 10:
            position = 10

        if position < 100:
            # oii ser.write('0' + str.encode(str(position)))
            print("<100")
        elif position < 10:
            # oii ser.write('0' + '0' + str.encode(str(position)))
            print("<10")
        else:
            # oii ser.write(str.encode(str(position)))
            print(">100")

        #kepala akhir

        if position <= 85:
            data = "D"
            print("BELOK KANAN")
        if position >= 95:
            data = "A"
            print("BELOK KIRI")
        if 85 < position < 95:
            print("break")

            # Mengupdate data hanya jika terjadi perubahan
        if (data1 != data):
            data1 = data

        cv2.imshow("Frame", frame)
        cv2.imshow("contours", thresh)

        cv2.waitKey(1) & 0xFF


delay = 200  ###for 10 seconds delay
sekarang = time.time()
close_time = time.time() + delay
while True:
    B()
    A()
    if time.time() > close_time:
        break
cv2.destroyAllWindows()