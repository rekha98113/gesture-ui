import cv2
import mediapipe as mp
import pyautogui
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

SCROLL_THRESHOLD = 0.05
MOVEMENT_THRESHOLD = 0.01
prev_y = None

def distance(p1, p2):
    return math.hypot(p2.x - p1.x, p2.y - p1.y)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        lm = hand.landmark

        index_tip = lm[8]
        middle_tip = lm[12]

        dist = distance(index_tip, middle_tip)

        if dist < SCROLL_THRESHOLD:

            current_y = index_tip.y

            if prev_y is not None:
                delta = current_y - prev_y

                # Scroll Down
                if delta > MOVEMENT_THRESHOLD:
                    pyautogui.scroll(-40)
                    print("Scrolling Down")

                # Scroll Up
                elif delta < -MOVEMENT_THRESHOLD:
                    pyautogui.scroll(40)
                    print("Scrolling Up")

            prev_y = current_y

        else:
            prev_y = None

    cv2.imshow("Scroll Up & Down Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()