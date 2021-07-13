import cv2
import numpy as np
#import serial

#ser = serial.Serial("/dev/OpenCM9.04", 9600)  # Open port with baud rate
# data = 0

cap = cv2.VideoCapture(0)
# Set camera resolution
cap.set(3, 480)  # 3,480
cap.set(4, 320)  # 4,320
_, frame = cap.read()
rows, cols, _ = frame.shape

x_medium = int(cols / 2)
center = int(cols / 2)
position = 90  # degrees

while True:
    _, frame = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert to HSV
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Make Yellow Color Range
    lower_led = np.array([161, 155, 84])
    upper_led = np.array([179, 255, 255])

    # Make Yellow Mask
    mask_yellow = cv2.inRange(img_hsv, lower_led, upper_led)

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

    contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)[-2:]
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)

        x_medium = int((x + x + w) / 2)
        break

    cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)

    # Move servo motor
    if x_medium < center - 40:
        position += 2

    if x_medium > center + 40:
        position -= 2

    if position > 180:
        position = 180
    if position < 10:
        position = 10

    cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
    print(x_medium, position)

    if position < 100:
        print("100")
        #ser.write('0' + str.encode(str(position)))

    elif position < 10:
        print("100")
        #ser.write('0' + '0' + str.encode(str(position)))

    else:
        print("100")
        #ser.write(str.encode(str(position)))

    cv2.imshow("Frame", frame)
    cv2.imshow("2", thresh)
    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()