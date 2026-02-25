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

last_click_time = 0
CLICK_DELAY = 0.8  # seconds

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

        # Index finger
        index_tip = hand.landmark[8]
        ix, iy = int(index_tip.x * w), int(index_tip.y * h)

        # Thumb
        thumb_tip = hand.landmark[4]
        tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)

        # Move mouse
        pyautogui.moveTo(
            int(index_tip.x * screen_w),
            int(index_tip.y * screen_h)
        )

        # Distance between thumb & index
        distance = math.hypot(ix - tx, iy - ty)

        # Draw points
        cv2.circle(frame, (ix, iy), 8, (0, 255, 0), -1)
        cv2.circle(frame, (tx, ty), 8, (0, 0, 255), -1)

        # Click condition
        current_time = time.time()
        if distance < 30 and (current_time - last_click_time) > CLICK_DELAY:
            pyautogui.click()
            last_click_time = current_time

    cv2.imshow("STEP 4 - Move + Click", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
