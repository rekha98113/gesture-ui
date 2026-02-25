import cv2
import mediapipe as mp
import pyautogui
import time

screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0
SMOOTHING = 7

last_left = 0
last_right = 0
DELAY = 1.0

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

        # Cursor movement
        target_x = index_tip.x * screen_w
        target_y = index_tip.y * screen_h

        curr_x = prev_x + (target_x - prev_x) / SMOOTHING
        curr_y = prev_y + (target_y - prev_y) / SMOOTHING
        pyautogui.moveTo(curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y

        # Finger states
        index_up = index_tip.y < index_joint.y
        middle_up = middle_tip.y < middle_joint.y
        ring_up = ring_tip.y < ring_joint.y

        now = time.time()

        # LEFT CLICK → index only
        if index_up and not middle_up and not ring_up and (now - last_left) > DELAY:
            pyautogui.click()
            last_left = now
            cv2.putText(frame, "LEFT CLICK", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

        # RIGHT CLICK → index + middle
        elif index_up and middle_up and not ring_up and (now - last_right) > DELAY:
            pyautogui.rightClick()
            last_right = now
            cv2.putText(frame, "RIGHT CLICK", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

    cv2.imshow("Virtual Mouse - Fixed Right Click", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
