import cv2
import mediapipe as mp
camera = cv2.VideoCapture(0)
while True:
    success, img = camera.read()
    if success:
        img = cv2.flip(img,1)
        cv2.imshow('Video',img)
    k = cv2.waitKey(1)
    if k== ord('z'):
        break
camera.release()