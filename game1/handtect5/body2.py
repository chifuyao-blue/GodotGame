import cv2
import mediapipe as mp
from handUtils import HandDetector

#camera = cv2.VideoCapture(0)
# Initialize mediapipe pose class.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_hands = mp.solutions.hands
hand_dector = mp_hands.Hands()

# Initialize mediapipe drawing class, useful for annotation.
mp_drawing = mp.solutions.drawing_utils

# Load the video file.
cap = cv2.VideoCapture(0)

# Check if the video is opened successfully.
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Reached the end of the video.")
        break
    frame = cv2.flip(frame,1)
    # Convert the BGR image to RGB.
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and detect the pose.
    result = pose.process(image_rgb)
    result2 = hand_dector.process(image_rgb)

    # Draw the pose annotation on the image.
    if result.pose_landmarks:
        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    if result2.multi_hand_landmarks:
        for handlms in result2.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, handlms, mp_hands.HAND_CONNECTIONS)
    # Display the frame with pose landmarks.
    cv2.imshow('Pose Estimation', frame)

    # Break the loop if 'q' is pressed.
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release the video capture object and close display window.
cap.release()
cv2.destroyAllWindows()

