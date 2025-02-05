import cv2
import mediapipe as mp
import time
import numpy as np
from pynput.mouse import Controller, Button
import threading

mouse = Controller()

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture("http://192.168.68.101:4747/video")
holistic = mp_holistic.Holistic(
    static_image_mode=False,
    model_complexity=0,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

prev_wrist_pos = {"left": None, "right": None}
threshold = 30  # Adjust to fine-tune punch sensitivity
cooldown = 0.3  # time it takes to make a punch
last_punch_time = {"left": 0, "right": 0}


def click_mouse(left_button=True):
    mouse.press(Button.left if left_button else Button.right)
    threading.Timer(
        0.05, mouse.release, args=[Button.left if left_button else Button.right]
    ).start()


def is_punching(prev_pos, new_pos):
    if prev_pos is None or new_pos is None:
        return False

    movement = np.linalg.norm(np.array(new_pos) - np.array(prev_pos))
    return movement > threshold


while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = holistic.process(frame_rgb)

    if results.pose_landmarks:
        left_wrist = results.pose_landmarks.landmark[
            mp_holistic.PoseLandmark.LEFT_WRIST
        ]
        right_wrist = results.pose_landmarks.landmark[
            mp_holistic.PoseLandmark.RIGHT_WRIST
        ]

        left_wrist_pos = (left_wrist.x * frame.shape[1], left_wrist.y * frame.shape[0])
        right_wrist_pos = (
            right_wrist.x * frame.shape[1],
            right_wrist.y * frame.shape[0],
        )

        if is_punching(prev_wrist_pos["left"], left_wrist_pos):
            current_time = time.time()
            if current_time - last_punch_time["left"] > cooldown:
                click_mouse()
                print("Left Punch!")
                last_punch_time["left"] = current_time

        if is_punching(prev_wrist_pos["right"], right_wrist_pos):
            current_time = time.time()
            if current_time - last_punch_time["left"] > cooldown:
                click_mouse(False)
                print("Right Punch!")
                last_punch_time["right"] = current_time

        prev_wrist_pos["left"] = left_wrist_pos
        prev_wrist_pos["right"] = right_wrist_pos

    mp_drawing.draw_landmarks(
        frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS
    )

    cv2.imshow("Boxing Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
