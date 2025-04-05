import cv2
import mediapipe as mp
#调用摄像头
camra = cv2.VideoCapture(0)
hand_dector = mp.solutions.hands.Hands()
while True:
    success, img  = camra.read()
    if success:
        img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        result = hand_dector.process(img_rgb)
        if result.multi_hand_landmarks:
            for handlms in result.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(img,handlms,mp.solutions.hands.HAND_CONNECTIONS)
        cv2.imshow('Video',img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
camra.release()
cv2.destroyAllWindows()