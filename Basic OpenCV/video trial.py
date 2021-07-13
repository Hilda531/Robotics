import cv2

cap = cv2.VideoCapture(0)
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#cap.set(3, 640)
#cap.set(4, 480)
print(cap.get(3))
print(cap.get(4))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:

        font = cv2.FONT_HERSHEY_DUPLEX
        text = 'Width:' + str(cap.get(3)), 'Height:' + str(cap.get(4))
        frame = cv2.putText(frame, text, (10, 50), font, 1, (50, 250, 255), 4)

        cv2.imshow('frame', frame)
        j = cv2.waitKey(1) & 0xFF
        if j == ord('o'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()