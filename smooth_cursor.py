import cv2
import mediapipe as mp
import pyautogui
import math
import time

screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0
SMOOTHING = 7

last_click_time = 0
CLICK_DELAY = 0.8

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

        index_tip = hand.landmark[8]
        thumb_tip = hand.landmark[4]

        target_x = index_tip.x * screen_w
        target_y = index_tip.y * screen_h

        # Smooth movement
        curr_x = prev_x + (target_x - prev_x) / SMOOTHING
        curr_y = prev_y + (target_y - prev_y) / SMOOTHING

        pyautogui.moveTo(curr_x, curr_y)

        prev_x, prev_y = curr_x, curr_y

        # Click logic
        ix, iy = int(index_tip.x * w), int(index_tip.y * h)
        tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)
        distance = math.hypot(ix - tx, iy - ty)

        current_time = time.time()
        if distance < 30 and (current_time - last_click_time) > CLICK_DELAY:
            pyautogui.click()
            last_click_time = current_time

    cv2.imshow("STEP 5 - Smooth Virtual Mouse", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
