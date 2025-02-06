import mediapipe as mp
import numpy as np

from modules.config_loader import ConfigLoader


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

    def is_punching(self, prev_pos, new_pos):
        if prev_pos is None or new_pos is None:
            return False

        movement = np.linalg.norm(np.array(new_pos) - np.array(prev_pos))
        return movement > self.app_config.threshold
