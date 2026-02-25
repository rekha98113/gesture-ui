import cv2
import mediapipe as mp
import pyautogui
import time

screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

cap = cv2.VideoCapture(0)

prev_y = 0
SCROLL_THRESHOLD = 10     # sensitivity
SCROLL_SPEED = 200
         # amount per scroll

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

        # Landmarks
        index_tip = hand.landmark[8]
        index_joint = hand.landmark[6]

        middle_tip = hand.landmark[12]
        middle_joint = hand.landmark[10]

        ring_tip = hand.landmark[16]
        ring_joint = hand.landmark[14]

        # Finger states
        index_up = index_tip.y < index_joint.y
        middle_up = middle_tip.y < middle_joint.y
        ring_up = ring_tip.y < ring_joint.y

        # Cursor move (index finger)
        pyautogui.moveTo(
            int(index_tip.x * screen_w),
            int(index_tip.y * screen_h)
        )

        # -------- SCROLL MODE --------
        if index_up and middle_up and not ring_up:
            current_y = int(index_tip.y * h)

            if prev_y != 0:
                delta = prev_y - current_y

                if abs(delta) > SCROLL_THRESHOLD:
                    if delta > 0:
                        pyautogui.scroll(SCROLL_SPEED)   # scroll up
                    else:
                        pyautogui.scroll(-SCROLL_SPEED)  # scroll down

            prev_y = current_y
        else:
            prev_y = 0  # reset when not in scroll mode

    cv2.imshow("Gesture UI - Scroll Enabled", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
