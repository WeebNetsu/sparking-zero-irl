import math

import mediapipe as mp
import numpy as np

from modules.config_loader import ConfigLoader
from modules.position import Position


class PoseTracker:
    def __init__(self, app_config: ConfigLoader):
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils
        self.holistic = self.mp_holistic.Holistic(
            static_image_mode=False,
            model_complexity=0,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.app_config = app_config

    def is_punching(self, prev_pos: Position, new_pos: Position):
        if prev_pos.has_none_values() or new_pos.has_none_values():
            return False

        movement = np.linalg.norm(
            np.array(new_pos.to_tuple()) - np.array(prev_pos.to_tuple())
        )
        return movement > self.app_config.threshold

    def is_recharging(
        self,
        left_wrist_pos: Position,
        right_wrist_pos: Position,
        left_hip_pos: Position,
        right_hip_pos: Position,
    ):
        if (
            left_wrist_pos.has_none_values()
            or right_wrist_pos.has_none_values()
            or left_hip_pos.has_none_values()
            or right_hip_pos.has_none_values()
        ):
            return False

        # Calculate Euclidean distances between wrist and hip positions
        left_distance = math.dist(left_wrist_pos.to_tuple(), left_hip_pos.to_tuple())
        right_distance = math.dist(right_wrist_pos.to_tuple(), right_hip_pos.to_tuple())

        # Check if both distances are within the threshold
        if left_distance <= 130 and right_distance <= 130:
            return True

        return False
