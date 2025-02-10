import time
from typing import Literal

import cv2

from modules.config_loader import ConfigLoader
from modules.keyboard_actions import KeyboardActions
from modules.pose_tracker import PoseTracker
from modules.position import Position
from modules.sides import Sides


class App:
    def __init__(self, app_config: ConfigLoader):
        self.app_config = app_config
        self.keyboard = KeyboardActions()
        self.pose_tracker = PoseTracker(app_config)
        self.cap = cv2.VideoCapture(app_config.webcam)
        self.prev_wrist_pos = Sides(Position(None, None), Position(None, None))

    def get_limb_position(self, limb_x, limb_y, frame):
        return Position(
            limb_x * frame.shape[1],
            limb_y * frame.shape[0],
        )

    def detect_punches(
        self, prev_pos: Position, new_pos: Position, hand_side: Literal["left", "right"]
    ):
        """Detect punches based on wrist positions."""
        if self.pose_tracker.is_punching(prev_pos, new_pos):
            current_time = time.time()
            hand_time = (
                self.prev_wrist_pos.left_time
                if hand_side == "left"
                else self.prev_wrist_pos.right_time
            )
            if current_time - hand_time > self.pose_tracker.app_config.cooldown:
                self.keyboard.click_mouse(left_button=(hand_side == "left"))
                if self.app_config.debug:
                    print(f"{hand_side.capitalize()} Punch!")

                if hand_side == "left":
                    self.prev_wrist_pos.left_time = current_time
                else:
                    self.prev_wrist_pos.right_time = current_time

    def detect_recharge(
        self,
        left_wrist_pos: Position,
        right_wrist_pos: Position,
        left_hip_pos: Position,
        right_hip_pos: Position,
    ):
        """Detect recharge based on wrist and hip positions."""
        if self.pose_tracker.is_recharging(
            left_wrist_pos, right_wrist_pos, left_hip_pos, right_hip_pos
        ):
            self.keyboard.hold_shift()
        else:
            self.keyboard.release_shift()

    def process_frame(self, frame):
        """Process each frame for pose landmarks and punch detection."""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose_tracker.holistic.process(frame_rgb)

        if not results.pose_landmarks:
            return

        left_hip = results.pose_landmarks.landmark[
            self.pose_tracker.mp_holistic.PoseLandmark.LEFT_HIP
        ]
        right_hip = results.pose_landmarks.landmark[
            self.pose_tracker.mp_holistic.PoseLandmark.RIGHT_HIP
        ]
        left_wrist = results.pose_landmarks.landmark[
            self.pose_tracker.mp_holistic.PoseLandmark.LEFT_WRIST
        ]
        right_wrist = results.pose_landmarks.landmark[
            self.pose_tracker.mp_holistic.PoseLandmark.RIGHT_WRIST
        ]

        # frame.shape is the width and height of the image
        left_wrist_pos = self.get_limb_position(left_wrist.x, left_wrist.y, frame)
        right_wrist_pos = self.get_limb_position(right_wrist.x, right_wrist.y, frame)
        left_hip_pos = self.get_limb_position(left_hip.x, left_hip.y, frame)
        right_hip_pos = self.get_limb_position(right_hip.x, right_hip.y, frame)

        self.detect_punches(self.prev_wrist_pos.left, left_wrist_pos, "left")
        self.detect_punches(self.prev_wrist_pos.right, right_wrist_pos, "right")

        self.detect_recharge(
            left_wrist_pos, right_wrist_pos, left_hip_pos, right_hip_pos
        )

        self.prev_wrist_pos.left = left_wrist_pos
        self.prev_wrist_pos.right = right_wrist_pos

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
