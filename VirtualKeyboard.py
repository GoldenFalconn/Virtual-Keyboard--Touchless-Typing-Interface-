import cv2
import numpy as np
import time
import mediapipe as mp

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Screen setup
screen_w, screen_h = 1280, 720
key_size = (100, 100)
font = cv2.FONT_HERSHEY_SIMPLEX

# Key hover config
hover_delay = 2.5  # seconds

# Global states
typed_text = ""
hover_start = 0
hovering_key = None
key_locked = False

# Key definitions
keys = [
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    list("ZXCVBNM"),
    ["SPACE", "BACK", "CLEAR"]
]

# Key layout calculation
def get_keyboard_layout():
    layout = []
    y_offset = 100
    for row in keys:
        row_layout = []
        x_offset = (screen_w - len(row) * (key_size[0] + 20)) // 2
        for key in row:
            rect = (x_offset, y_offset, key_size[0], key_size[1])
            row_layout.append((key, rect))
            x_offset += key_size[0] + 20
        layout.append(row_layout)
        y_offset += key_size[1] + 20
    return layout

keyboard_layout = get_keyboard_layout()

# Draw keyboard
def draw_keyboard(img, layout, fingertip=None):
    global hovering_key, hover_start, key_locked

    key_hovered_now = None

    for row in layout:
        for key, (x, y, w, h) in row:
            color = (180, 180, 180)
            if fingertip and x < fingertip[0] < x + w and y < fingertip[1] < y + h:
                color = (0, 255, 0)
                key_hovered_now = key
                if hovering_key == key and not key_locked:
                    elapsed = time.time() - hover_start
                    if elapsed >= hover_delay:
                        handle_key_press(key)
                        key_locked = True
                elif hovering_key != key:
                    hovering_key = key
                    hover_start = time.time()
            elif hovering_key == key:
                # Reset if moved away
                hovering_key = None
                hover_start = 0
                key_locked = False

            cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)
            cv2.putText(img, key, (x + 10, y + 60), font, 1, (0, 0, 0), 2)

            # Progress indicator
            if fingertip and key == key_hovered_now and not key_locked:
                elapsed = time.time() - hover_start
                pct = min(elapsed / hover_delay, 1.0)
                bar_w = int(w * pct)
                cv2.rectangle(img, (x, y + h - 10), (x + bar_w, y + h), (0, 0, 255), -1)

# Key handling
def handle_key_press(key):
    global typed_text
    if key == "SPACE":
        typed_text += " "
    elif key == "BACK":
        typed_text = typed_text[:-1]
    elif key == "CLEAR":
        typed_text = ""
    else:
        typed_text += key

# Main loop
cap = cv2.VideoCapture(0)
cap.set(3, screen_w)
cap.set(4, screen_h)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    fingertip_pos = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark[8]  # Index finger tip
            h, w, _ = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            fingertip_pos = (cx, cy)
            cv2.circle(frame, (cx, cy), 10, (255, 0, 255), -1)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    draw_keyboard(frame, keyboard_layout, fingertip=fingertip_pos)

    # Draw typed text area
    cv2.rectangle(frame, (50, screen_h - 120), (screen_w - 50, screen_h - 50), (255, 255, 255), -1)
    cv2.putText(frame, typed_text, (60, screen_h - 70), font, 1.5, (0, 0, 0), 3)

    cv2.imshow("Virtual Keyboard", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
