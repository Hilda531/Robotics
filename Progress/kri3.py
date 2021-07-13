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
video_capture1 = cv2.VideoCapture(0)
video_capture2 = cv2.VideoCapture(0)
sleep(0.3)
ctx = 0
cty = 0
cy = 0
cx = 0
a = 1
video_capture1.set(3, 1920)
video_capture1.set(4, 1080)
video_capture2.set(3, 640)
video_capture2.set(4, 480)

# Serial Communication Initialization
#ser = serial.Serial("/dev/ttyS0", 9600)  # Open port with baud rate
# ser = serial.Serial ("COM13", 9600)


delay=10    ###for 10 seconds delay
close_time=time.time()+delay
while (True):

    # Capture the frames
    ret, frame1 = video_capture1.read()

    # Crop the image
    crop_img1 = frame1[180:720, 640:1280]

    # Convert to grayscale
    gray = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2GRAY)

    # Convert to HSV
    img_hsv = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2HSV)

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
        cv2.line(crop_img1, (cx, 0), (cx, 720), (255, 0, 0), 1)
        cv2.line(crop_img1, (0, cy), (1280, cy), (255, 0, 0), 1)
        cv2.drawContours(crop_img1, contours, -1, (0, 255, 0), 1)
        print(cx)
        data = int(cx)

    # Mengupdate data hanya jika terjadi perubahan
    if (data1 != data):
        data1 = data
        # Mengirim data secara serial
#        ser.write([data])
    # Display the resulting frame
    cv2.imshow('mask_yw_image', mask_yw_image)
    cv2.imshow('contours', thresh)
    cv2.imshow('frame', crop_img1)

    if cv2.waitKey(1) & 0xFF :
        if time.time() > close_time :
            break


delay=10    ###for 10 seconds delay
close_time=time.time()+delay
while (True):

    # Capture the frames
    ret, frame2 = video_capture2.read()

    # Crop the image
    crop_img2 = frame2[80:320, 0:640]

    # Convert to grayscale
    gray = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2GRAY)

    # Convert to HSV
    img_hsv = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2HSV)

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
        cv2.line(crop_img2, (cx, 0), (cx, 720), (255, 0, 0), 1)
        cv2.line(crop_img2, (0, cy), (1280, cy), (255, 0, 0), 1)
        cv2.drawContours(crop_img2, contours, -1, (0, 255, 0), 1)
        print(cx)
        data = int(cx)

    # Mengupdate data hanya jika terjadi perubahan
    if (data1 != data):
        data1 = data
        # Mengirim data secara serial
#        ser.write([data])
    # Display the resulting frame
    cv2.imshow('mask_yw_image', mask_yw_image)
    cv2.imshow('contours', thresh)
    cv2.imshow('frame', crop_img2)

    if cv2.waitKey(1) & 0xFF :
        if time.time() > close_time :
            break


delay=5    ###for 5 seconds delay
close_time=time.time()+delay
while True:
    #Kepiting Kiri
    print("LEFTS!")
    data = 'F'
    if (data1 != data):
        data1 = data
       # Mengirim data secara serial
#        ser.write(str.encode(data1))
    if time.time()>close_time:
         break

delay=10    ###for 10 seconds delay
close_time=time.time()+delay
while True:
    #Maju
    print("FORWARD!")
    data = 'W'
    if (data1 != data):
        data1 = data
       # Mengirim data secara serial
#        ser.write(str.encode(data1))
    if time.time()>close_time:
         break

delay=10    ###for 10 seconds delay
close_time=time.time()+delay
while True:
    #Kepiting Kanan
    print("RIGHTS!")
    data = 'G'
    if (data1 != data):
        data1 = data
       # Mengirim data secara serial
#        ser.write(str.encode(data1))
    if time.time()>close_time:
         break

delay=5    ###for 10 seconds delay
close_time=time.time()+delay
while True:
    #Putar Balik
    print("ROUND!")
    data = 'R'
    if (data1 != data):
        data1 = data
       # Mengirim data secara serial
#        ser.write(str.encode(data1))
    if time.time()>close_time:
         break

delay=10    ###for 10 seconds delay
close_time=time.time()+delay
while (True):

    # Capture the frames
    ret, frame1 = video_capture1.read()

    # Crop the image
    crop_img1 = frame1[180:720, 640:1280]

    # Convert to grayscale
    gray = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2GRAY)

    # Convert to HSV
    img_hsv = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2HSV)

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
        cv2.line(crop_img1, (cx, 0), (cx, 720), (255, 0, 0), 1)
        cv2.line(crop_img1, (0, cy), (1280, cy), (255, 0, 0), 1)
        cv2.drawContours(crop_img1, contours, -1, (0, 255, 0), 1)
        print(cx)
        data = int(cx)

    # Mengupdate data hanya jika terjadi perubahan
    if (data1 != data):
        data1 = data
        # Mengirim data secara serial
#        ser.write([data])
    # Display the resulting frame
    cv2.imshow('mask_yw_image', mask_yw_image)
    cv2.imshow('contours', thresh)
    cv2.imshow('frame', crop_img1)

    if cv2.waitKey(1) & 0xFF :
        if time.time() > close_time :
            break
frame1.release()


delay=10    ###for 10 seconds delay
close_time=time.time()+delay
while (True):

    # Capture the frames
    ret, frame2 = video_capture2.read()

    # Crop the image
    crop_img2 = frame2[80:320, 0:640]

    # Convert to grayscale
    gray = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2GRAY)

    # Convert to HSV
    img_hsv = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2HSV)

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
        cv2.line(crop_img2, (cx, 0), (cx, 720), (255, 0, 0), 1)
        cv2.line(crop_img2, (0, cy), (1280, cy), (255, 0, 0), 1)
        cv2.drawContours(crop_img2, contours, -1, (0, 255, 0), 1)
        print(cx)
        data = int(cx)

    # Mengupdate data hanya jika terjadi perubahan
    if (data1 != data):
        data1 = data
        # Mengirim data secara serial
#        ser.write([data])
    # Display the resulting frame
    cv2.imshow('mask_yw_image', mask_yw_image)
    cv2.imshow('contours', thresh)
    cv2.imshow('frame', crop_img2)

    if cv2.waitKey(1) & 0xFF :
        if time.time() > close_time :
            break
frame2.release()
cv2.destroyAllWindows()

delay=5    ###for 10 seconds delay
close_time=time.time()+delay
while True:
    #STOP
    print("STOP!")
    data = 'P'
    if (data1 != data):
        data1 = data
       # Mengirim data secara serial
#        ser.write(str.encode(data1))
    if time.time()>close_time:
         break