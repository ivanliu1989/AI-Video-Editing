import cv2
img = cv2.imread("../mmexport1545548449041.jpg")

while True:
    cv2.imshow('Ivan', img)
    
    # IF we've waited at least 1ms AND we've pressed the Esc
    if cv2.waitKey(1) & 0xff == 27:
        break

cv2.destroyAllWindows()