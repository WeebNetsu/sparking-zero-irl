from modules.config_loader import ConfigLoader
from modules.keyboard_actions import KeyboardActions
from modules.pose_tracker import PoseTracker
import cv2
import time


class App:
    def __init__(self, app_config: ConfigLoader):
        self.keyboard = KeyboardActions()
        self.pose_tracker = PoseTracker(app_config)
        self.cap = cv2.VideoCapture(app_config.webcam)
        self.prev_wrist_pos = {"left": None, "right": None}
        self.last_punch_time = {"left": 0, "right": 0}

    def detect_punches(self, prev_pos, new_pos, hand_side):
        """Detect punches based on wrist positions."""
        if self.pose_tracker.is_punching(prev_pos, new_pos):
            current_time = time.time()
            if (
                current_time - self.last_punch_time[hand_side]
                > self.pose_tracker.app_config.cooldown
            ):
                self.keyboard.click_mouse(left_button=(hand_side == "left"))
                print(f"{hand_side.capitalize()} Punch!")
                self.last_punch_time[hand_side] = current_time

    def process_frame(self, frame):
        """Process each frame for pose landmarks and punch detection."""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose_tracker.holistic.process(frame_rgb)

        if results.pose_landmarks:
            left_wrist = results.pose_landmarks.landmark[
                self.pose_tracker.mp_holistic.PoseLandmark.LEFT_WRIST
            ]
            right_wrist = results.pose_landmarks.landmark[
                self.pose_tracker.mp_holistic.PoseLandmark.RIGHT_WRIST
            ]

            left_wrist_pos = (
                left_wrist.x * frame.shape[1],
                left_wrist.y * frame.shape[0],
            )
            right_wrist_pos = (
                right_wrist.x * frame.shape[1],
                right_wrist.y * frame.shape[0],
            )

            self.detect_punches(self.prev_wrist_pos["left"], left_wrist_pos, "left")
            self.detect_punches(self.prev_wrist_pos["right"], right_wrist_pos, "right")

            self.prev_wrist_pos["left"] = left_wrist_pos
            self.prev_wrist_pos["right"] = right_wrist_pos

            self.pose_tracker.mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.pose_tracker.mp_holistic.POSE_CONNECTIONS,
            )

    def run(self):
        """Main loop to run the boxing detection app."""
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                break

            self.process_frame(frame)

            cv2.imshow("Boxing Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()
