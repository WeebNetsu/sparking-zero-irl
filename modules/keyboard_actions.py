import threading
from pynput.mouse import Controller, Button


class KeyboardActions:
    def __init__(self):
        self.mouse = Controller()

    def click_mouse(self, left_button=True):
        self.mouse.press(Button.left if left_button else Button.right)
        threading.Timer(
            0.05,
            self.mouse.release,
            args=[Button.left if left_button else Button.right],
        ).start()
