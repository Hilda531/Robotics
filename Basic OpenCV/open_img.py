import cv2

img = cv2.imread('apple.jpg', 1)

print(img)
cv2.imshow('image', img)
j = cv2.waitKey(0)

if j == 27:
    cv2.destroyAllWindows()
elif j == ord('o'):
    cv2.imwrite('imgcopy.png', img)
    cv2.destroyAllWindows()