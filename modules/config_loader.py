import json
from typing import Any, List
from pathlib import Path


class ConfigLoader:
    def __init__(
        self,
        config_file_paths: List[str] = [
            "configs/app_config.json",
            "configs/computer_info.json",
        ],
    ):
        self.threshold: int = 30
        self.cooldown: float = 0.3
        self.webcam: int | str = 0

        for file_path in config_file_paths:
            if not Path(file_path).is_file():
                print(
                    f"Warning: Config file {file_path} not found, skipping and loading defaults."
                )
                continue

            with open(file_path, "r") as config:
                json_data = json.loads(config.read())

                self._update_config(json_data)

    def _update_config(self, json_data):
        """Update attributes only if they exist in the config."""

        def is_valid_type(key: str, data: Any, expected_type: type):
            if not isinstance(data, expected_type):
                print(f"{key} is not of type {expected_type.__name__}, skipping")
                return False
            return True

        if "threshold" in json_data:
            data = json_data["threshold"]
            if is_valid_type("threshold", data, int):
                self.threshold = data

        if "cooldown" in json_data:
            data = json_data["cooldown"]
            if is_valid_type("cooldown", data, float):
                self.cooldown = data

        if "webcam" in json_data:
            data = json_data["webcam"]
            if is_valid_type("webcam", data, int | str):
                self.webcam = data
