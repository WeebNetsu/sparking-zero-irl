import threading

from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController


class KeyboardActions:
    def __init__(self):
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

    def click_mouse(self, left_button=True):
        self.mouse.press(Button.left if left_button else Button.right)
        threading.Timer(
            0.05,
            self.mouse.release,
            args=[Button.left if left_button else Button.right],
        ).start()

    def hold_shift(self):
        self.keyboard.press(Key.shift)

    def release_shift(self):
        self.keyboard.release(Key.shift)  # Release the Shift key
