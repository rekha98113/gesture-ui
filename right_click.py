import cv2
import mediapipe as mp
import pyautogui
import math

screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

dragging = False
right_pinch_active = False   # Track thumb-pinky pinch state

def distance(p1, p2):
    return math.hypot(p2.x - p1.x, p2.y - p1.y)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        lm = hand.landmark

        thumb_tip = lm[4]
        index_tip = lm[8]
        pinky_tip = lm[20]

        # -------- Cursor Movement --------
        screen_x = int(index_tip.x * screen_w)
        screen_y = int(index_tip.y * screen_h)
        pyautogui.moveTo(screen_x, screen_y)

        # -------- Distances --------
        dist_thumb_index = distance(thumb_tip, index_tip)
        dist_thumb_pinky = distance(thumb_tip, pinky_tip)

        # -------- LEFT DRAG (Thumb + Index) --------
        if dist_thumb_index < 0.05:
            if not dragging:
                pyautogui.mouseDown()
                dragging = True
        else:
            if dragging:
                pyautogui.mouseUp()
                dragging = False

        # -------- RIGHT CLICK (Thumb + Pinky Pinch & Release) --------
        if dist_thumb_pinky < 0.05:
            right_pinch_active = True   # Pinch detected

        elif right_pinch_active:
            # Release detected → trigger right click
            pyautogui.rightClick()
            print("Right Click")
            right_pinch_active = False

    cv2.imshow("Gesture Mouse Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()