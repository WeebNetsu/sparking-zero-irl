import cv2
import hand_tracking as hdm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# import pyautogui
from pynput.mouse import Controller, Button

mouse = Controller()
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

min_finger_distance = 50
max_finger_distance = 300
clicking = False  # Track whether mouse is currently held down

# get webcam
cap = cv2.VideoCapture("http://192.168.101.102:4747/video")

if not cap.isOpened():
    print("Error: Couldn't open webcam")
    exit()

detector = hdm.HandDetector(
    detection_con=0.5,
    model_complexity=0,
    max_hands=1,
)

while True:
    success, img = cap.read()

    if not success:
        print("Error: Couldn't read frame")
        break

    img = detector.find_hands(img, True)

    landmarks_list = detector.find_position(img)
    if len(landmarks_list) != 0:
        # landmark 4 is thumb
        thumb_point = next(
            (landmark for landmark in landmarks_list if landmark.id == 4), None
        )

        hand_bottom_point = next(
            (landmark for landmark in landmarks_list if landmark.id == 2), None
        )

        if thumb_point and hand_bottom_point:
            center_x, center_y = (thumb_point.x_pos + hand_bottom_point.x_pos) // 2, (
                thumb_point.y_pos + hand_bottom_point.y_pos
            ) // 2

            cv2.circle(
                img, (thumb_point.x_pos, thumb_point.y_pos), 10, (255, 0, 0), cv2.FILLED
            )
            cv2.circle(
                img,
                (hand_bottom_point.x_pos, hand_bottom_point.y_pos),
                10,
                (255, 0, 0),
                cv2.FILLED,
            )
            cv2.line(
                img,
                (thumb_point.x_pos, thumb_point.y_pos),
                (hand_bottom_point.x_pos, hand_bottom_point.y_pos),
                (0, 255, 0),
                3,
            )
            cv2.circle(img, (center_x, center_y), 10, (0, 0, 255), cv2.FILLED)

            length = math.hypot(
                hand_bottom_point.x_pos - thumb_point.x_pos,
                hand_bottom_point.y_pos - thumb_point.y_pos,
            )

            if length <= min_finger_distance and not clicking:
                mouse.press(Button.left)
                # pyautogui.mouseDown()
                clicking = True
            elif length > min_finger_distance and clicking:
                mouse.release(Button.left)
                # pyautogui.mouseUp()
                clicking = False

    detector.add_fps_to_output(img)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
