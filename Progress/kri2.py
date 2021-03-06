import numpy as np
import cv2
#import serial
from time import sleep
import time

# Serial Communication Initialization
#ser = serial.Serial("/dev/OpenCM9.04", 9600)  # Open port with baud rate
# ser = serial.Serial ("COM13", 9600)

data = 'S'
data1 = 'A'
video_capture = cv2.VideoCapture(0)
sleep(0.3)
video_capture.set(3, 640)
video_capture.set(4, 480)
ctx = 0
cty = 0
cy = 0
cx = 0
a = 1

delay=35    ###for 45 seconds delay
close_time=time.time()+delay
while (True):

    # Capture the frames
    ret, frame = video_capture.read()

    # Crop the image
    crop_img = frame[80:320, 0:640]

    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Convert to HSV
    img_hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

    # Make Yellow Color Range
    lower_yellow = np.array([20, 100, 100], dtype="uint8")
    upper_yellow = np.array([30, 255, 255], dtype="uint8")

    # Make Yellow Mask
    mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

    # Make White Mask
    mask_white = cv2.inRange(gray, 200, 255)

    # Make Mask of White or Yellow
    mask_yw = cv2.bitwise_or(mask_white, mask_yellow)

    # Make Mask of Gray and (White or Yellow)
    mask_yw_image = cv2.bitwise_and(gray, mask_yw)

    # Gaussian blur
    blur = cv2.GaussianBlur(mask_yw_image, (5, 5), 0)

    # Color thresholding
    ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)

    # For delete noise
    # The erosion makes the object in white smaller.
    thresh = cv2.erode(thresh, None, iterations=2)
    # The dilatation makes the object in white bigger.
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find the contours of the frame
    contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        cty = cy
        if M['m00'] != 0:
            # Menentukan Center dari Contour
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
        cv2.line(crop_img, (cx, 0), (cx, 720), (255, 0, 0), 1)
        cv2.line(crop_img, (0, cy), (1280, cy), (255, 0, 0), 1)
        cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 1)

        if cx >= 512:
            print("Turn Right!")
            data = 'G'  # transmit data serially

        if cx < 384 and cx > 512:
            print("On Track!")
            data = 'W'

        if cx <= 384:
            print("Turn Left!")
            data = 'F'

        if time.time() > close_time:
            break

    else:
        print("I don't see the line")
        data = 'S'
    # Mengupdate data hanya jika terjadi perubahan
    if (data1 != data):
        data1 = data
        # Mengirim data secara serial
#        ser.write(str.encode(data1))

    # Display the resulting frame
    cv2.imshow('mask_yw_image', mask_yw_image)
    cv2.imshow('contours', thresh)
    cv2.imshow('frame', crop_img)
    if cv2.waitKey(1) & 0xFF:
        if time.time() > close_time:
            break

delay=3    ###for 15 seconds delay
close_time=time.time()+delay
while True:
    print("LEF!")
    data = 'F'
    if (data1 != data):
        data1 = data
        # Mengirim data secara serial
#        ser.write(str.encode(data1))
    if time.time()>close_time:
         break

delay=7.5    ###for 15 seconds delay
close_time=time.time()+delay
while True:
    print("FORWARD!")
    data = 'W'
    if (data1 != data):
        data1 = data
        # Mengirim data secara serial
#        ser.write(str.encode(data1))
    if time.time()>close_time:
         break

delay=5    ###for 15 seconds delay
close_time=time.time()+delay
while True:
    print("ROUND!")
    data = 'R'
    if (data1 != data):
        data1 = data
        # Mengirim data secara serial
#        ser.write(str.encode(data1))
    if time.time()>close_time:
         break

delay=40    ###for 45 seconds delay
close_time=time.time()+delay
while (True):

    # Capture the frames
    ret, frame = video_capture.read()

    # Crop the image
    crop_img = frame[80:320, 160:480]

    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Convert to HSV
    img_hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

    # Make Yellow Color Range
    lower_yellow = np.array([25, 0, 32], dtype="uint8")
    upper_yellow = np.array([151, 237, 255], dtype="uint8")

    # Make Yellow Mask
    mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

    # Make White Mask
    mask_white = cv2.inRange(gray, 200, 255)

    # Make Mask of White or Yellow
    mask_yw = cv2.bitwise_or(mask_white, mask_yellow)

    # Make Mask of Gray and (White or Yellow)
    mask_yw_image = cv2.bitwise_and(gray, mask_yw)

    # Make Mask of Gray and (White or Yellow)
    mask_yw_image2 = cv2.bitwise_not(mask_yw_image)

    # Gaussian blur
    blur = cv2.GaussianBlur(mask_yw_image2, (5, 5), 0)

    # Color thresholding
    ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)

    # For delete noise
    # The erosion makes the object in white smaller.
    thresh = cv2.erode(thresh, None, iterations=2)
    # The dilatation makes the object in white bigger.
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find the contours of the frame
    contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        cty = cy
        if M['m00'] != 0:
            # Menentukan Center dari Contour
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
        cv2.line(crop_img, (cx, 0), (cx, 720), (255, 0, 0), 1)
        cv2.line(crop_img, (0, cy), (1280, cy), (255, 0, 0), 1)
        cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 1)

        if cx >= 260:
            print("Turn Right!")
            data = 'R'  # transmit data serially

        if cx < 260 and cx > 140:
            print("On Track!")
            data = 'G'

        if cx <= 140:
            print("Turn Left")
            data = 'L'

    else:
        print("I don't see the line")
        data = 'S'

    # Mengupdate data hanya jika terjadi perubahan
    if (data1 != data):
        data1 = data
        # Mengirim data secara serial
#        ser.write(str.encode(data1))

    # Display the resulting frame
    cv2.imshow('mask_yw_image', mask_yw_image)
    cv2.imshow('contours', thresh)
    cv2.imshow('frame', crop_img)
    if cv2.waitKey(1) & 0xFF:
        if time.time() > close_time:
            break

delay=500    ###for 5 seconds delay
close_time=time.time()+delay
while True:
    print("STOP!")
    data = 'P'
    if (data1 != data):
        data1 = data
        # Mengirim data secara serial
#        ser.write(str.encode(data1))
    if time.time()>close_time:
         break