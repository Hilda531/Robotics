import numpy as np
import cv2

#img = np.zeros((500, 500, 3), np.uint8)
img = cv2.imread('apple.jpg')
cv2.imshow('image', img)

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        blue = img[y, x, 0]
        green = img[y, x, 1]
        red = img[y, x, 2]
        cv2.circle(img, (x, y), 2, (0, 0, 0), -1)
        color = np.zeros((500, 500, 3), np.uint8)
        color[:] = [blue, green, red]
        cv2.imshow('color', color)

cv2.setMouseCallback('image', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()
