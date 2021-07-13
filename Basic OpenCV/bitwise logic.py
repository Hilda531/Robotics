import numpy as np
import cv2

img = np.zeros((250, 250, 3), np.uint8)
img = cv2.rectangle(img, (125, 0), (250,250), (255, 255, 255), -1)
img2 = cv2.imread("chessboard.png")
img2 = cv2.resize(img2, (250, 250))

AND = cv2.bitwise_and(img, img2)
OR = cv2.bitwise_or(img, img2)
NOT = cv2.bitwise_not(img2)
XOR = cv2.bitwise_xor(img, img2)

cv2. imshow('and', AND)
cv2. imshow('or', OR)
cv2. imshow('not', NOT)
cv2. imshow('xor', XOR)
cv2. imshow('img', img)
cv2. imshow('img2', img2)

cv2.waitKey(0)
cv2.destroyAllWindows()