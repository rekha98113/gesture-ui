import cv2
import mediapipe as mp
import pyautogui
import math

# Get screen size
screen_w, screen_h = pyautogui.size()

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

# States
dragging = False
pinch_active = False

# Thresholds
PINCH_THRESHOLD = 0.05
DRAG_THRESHOLD = 0.04

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

        # Move cursor using index finger
        screen_x = int(index_tip.x * screen_w)
        screen_y = int(index_tip.y * screen_h)
        pyautogui.moveTo(screen_x, screen_y)

        dist = distance(thumb_tip, index_tip)

        # -------- Drag (Hold Strong Pinch) --------
        if dist < DRAG_THRESHOLD:
            if not dragging:
                pyautogui.mouseDown()
                dragging = True

        else:
            if dragging:
                pyautogui.mouseUp()
                dragging = False

        # -------- Left Click (Pinch + Release) --------
        if dist < PINCH_THRESHOLD and not dragging:
            pinch_active = True

        elif pinch_active:
            pyautogui.click()
            print("Left Click")
            pinch_active = False

    cv2.imshow("Left Click Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()