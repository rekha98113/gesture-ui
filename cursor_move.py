import cv2
import mediapipe as mp
import pyautogui

# Screen size
screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)  # mirror view (natural movement)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]

        # Index finger tip
        index_tip = hand.landmark[8]
        cx, cy = int(index_tip.x * w), int(index_tip.y * h)

        # Map to screen
        screen_x = int(index_tip.x * screen_w)
        screen_y = int(index_tip.y * screen_h)

        # Move mouse
        pyautogui.moveTo(screen_x, screen_y)

        # Visual feedback
        cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

    cv2.imshow("STEP 3 - Cursor Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
