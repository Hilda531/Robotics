import cv2
import numpy as np
#import serial ***
#import syslog
import statistics
from time import sleep
import time

#Lurus
def B():
    cap = cv2.VideoCapture(0)
    # Set camera resolution
    cap.set(3, 480)  # 3,480
    cap.set(4, 320)  # 4,320
    _, frame = cap.read()
    rows, cols, _ = frame.shape

    #coordinate
    y_medium = int(rows / 2)
    x_medium = int(cols / 2)

    while True:
        _, frame = cap.read()
        cv2.rectangle(frame, (210, 0), (430, 360), (10, 255, 10), 1)

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # red color (parameter + masking)
        low_red = np.array([161, 155, 84])
        high_red = np.array([179, 255, 255])
        red_mask = cv2.inRange(hsv_frame, low_red, high_red)
        _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)

            y_medium = int((y + y + h) / 2)
            x_medium = int((x + x + w) / 2)
            break

        cv2.line(frame, (x_medium, 0), (x_medium, 360), (255, 0, 0), 1)
        cv2.line(frame, (0, y_medium), (640, y_medium), (255, 0, 0), 1)

        #range bola
        if x_medium < 430 and x_medium > 210:
            print("On Track!")
            data = 'W'
        else:
            print("I don't see the line")
            break

        # Mengupdate data hanya jika terjadi perubahan
        if (data1 != data):
            data1 = data
        # Mengirim data secara serial
        # ser.write(str.encode(data1))
        cv2.imshow("Frame", frame)

        cv2.waitKey(1) & 0xFF

#Nengok
def A():
    # Serial Communication Initialization
    # ser = serial.Serial("/dev/OpenCM9.04", 9600)  # Open port with baud rate
    # ser = serial.Serial ("COM13", 9600)
    # data = 0

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
    mode = []

    while True:
        _, frame = cap.read()

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # red color
        low_red = np.array([161, 155, 84])
        high_red = np.array([179, 255, 255])
        red_mask = cv2.inRange(hsv_frame, low_red, high_red)
        _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 3)

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
        print(x_medium)

        #range servo
        if position > 180:
            position = 180
        if position < 10:
            position = 10

        #kepala akhir
        mode.append(int(position))
        modus = statistics.mode(mode)
        if modus == position:
            position = modus
            print(mode)
            if position <= 85:
                data = "D"
                print("HADAP KANAN")
            elif position >= 95:
                data = "A"
                print("HADAP KIRI")
            elif 85 < position < 95:
                print("break")
                break

        #Biar ngirim 3 angka ke servo
        if position < 100:
            # oii ser.write('0' + str.encode(str(int(position))))
            print("position = 0" + str(int(position)))
        elif position < 10:
            # oii ser.write('0' + '0' + str.encode(str(int(position))))
            print("position = 00" + str(int(position)))
        else:
            # oii ser.write(str.encode(str(int(position))))
            print(str(int(position)))


        # Mengupdate data hanya jika terjadi perubahan
        if (data1 != data):
            data1 = data
        # Mengirim data secara serial
        # ser.write(str.encode(data1))
        cv2.imshow("Frame", frame)

        cv2.waitKey(1) & 0xFF

#looping
delay = 200  ###for 10 seconds delay
sekarang = time.time()
close_time = time.time() + delay
while True:
    B()
    A()
    if time.time() > close_time:
        break
cv2.destroyAllWindows()