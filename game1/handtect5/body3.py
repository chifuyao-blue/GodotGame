import cv2
import mediapipe as mp

# 假设我们知道平均肩宽为0.45米（即45厘米）
KNOWN_DISTANCE = 0.45  # 实际肩宽距离
KNOWN_WIDTH_PIXELS = 150  # 在一定距离下肩宽对应的像素值


def find_distance(shoulder_width_pixels):
    # 使用相似三角形计算距离
    distance = (KNOWN_WIDTH_PIXELS * KNOWN_DISTANCE) / shoulder_width_pixels
    return distance


# Initialize MediaPipe pose and hands.
mp_pose = mp.solutions.pose.Pose()
mp_hands = mp.solutions.hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Open the camera for video capture.
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Reached the end of the video.")
        break

    frame = cv2.flip(frame, 1)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and detect pose and hands.
    result_pose = mp_pose.process(image_rgb)
    result_hands = mp_hands.process(image_rgb)

    if result_pose.pose_landmarks:
        # Draw pose landmarks on the frame.
        mp_drawing.draw_landmarks(frame, result_pose.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

        # Estimate distance based on shoulder width.
        left_shoulder = result_pose.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = result_pose.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]
        shoulder_width_pixels = ((left_shoulder.x - right_shoulder.x) ** 2 + (
                    left_shoulder.y - right_shoulder.y) ** 2) ** 0.5 * frame.shape[1]
        distance = find_distance(shoulder_width_pixels)
        cv2.putText(frame, f"Distance: {distance:.2f} m", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                    cv2.LINE_AA)

    if result_hands.multi_hand_landmarks:
        # Draw hand landmarks on the frame.
        for hand_landmarks in result_hands.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

    # Display the frame with annotations.
    cv2.imshow('Pose and Hand Detection', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()