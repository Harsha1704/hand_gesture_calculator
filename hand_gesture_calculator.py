import cv2
import numpy as np
import mediapipe as mp
import time

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Button setup
buttons = []
button_texts = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"]
]

colors = {
    "digits": (135, 206, 250),  # Light blue
    "ops": (255, 165, 0),       # Orange
    "hover": (50, 205, 50)      # Lime Green
}

# Button positions
for i in range(4):
    for j in range(4):
        x = 50 + j * 100
        y = 100 + i * 100
        text = button_texts[i][j]
        btn_type = "digits" if text.isdigit() else "ops"
        buttons.append({"pos": (x, y), "text": text, "type": btn_type})

# Expression variables
expression = ""
hover_start_time = None
hovering_button = None
click_delay = 1  

# Count fingers function
def count_fingers(hand_landmarks):
    tip_ids = [8, 12, 16, 20]
    fingers = 0
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers += 1
    for tip in tip_ids:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers += 1
    return fingers

# Draw circular button
def draw_button(img, x, y, text, color):
    cv2.circle(img, (x + 40, y + 40), 40, color, -1)
    cv2.circle(img, (x + 40, y + 40), 40, (255, 255, 255), 2)
    cv2.putText(img, text, (x + 22, y + 55), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    # Draw calculator box (background panel)
    cv2.rectangle(img, (30, 20), (470, 520), (0, 0, 0), -1)
    overlay = img.copy()
    alpha = 0.4  # Transparency factor
    cv2.rectangle(overlay, (30, 20), (470, 520), (0, 0, 0), -1)
    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

    # Outer border
    cv2.rectangle(img, (30, 20), (470, 520), (255, 255, 255), 2)

    # Expression display
    cv2.rectangle(img, (30, 20), (470, 80), (50, 50, 50), -1)
    cv2.rectangle(img, (30, 20), (470, 80), (255, 255, 255), 2)
    display_expr = expression[-16:]
    text_size = cv2.getTextSize(display_expr, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 2)[0]
    text_x = 460 - text_size[0]
    cv2.putText(img, display_expr, (text_x, 65), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

    if result.multi_hand_landmarks:
        handLms = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
        lm_list = [(int(lm.x * img.shape[1]), int(lm.y * img.shape[0])) for lm in handLms.landmark]

        if lm_list:
            x_finger, y_finger = lm_list[8]
            fingers = count_fingers(handLms)
            cv2.circle(img, (x_finger, y_finger), 10, (255, 0, 255), -1)

            if fingers == 5:
                hovered = False
                for btn in buttons:
                    x, y = btn["pos"]
                    dist = ((x_finger - (x + 40))**2 + (y_finger - (y + 40))**2)**0.5
                    if dist < 40:
                        draw_button(img, x, y, btn["text"], colors["hover"])
                        if hovering_button != btn:
                            hovering_button = btn
                            hover_start_time = time.time()
                        elif time.time() - hover_start_time >= click_delay:
                            char = btn["text"]
                            if char == "C":
                                expression = ""
                            elif char == "=":
                                try:
                                    expression = str(eval(expression))
                                except:
                                    expression = "Error"
                            else:
                                expression += char
                            hover_start_time = None
                            hovering_button = None
                        hovered = True
                    else:
                        draw_button(img, x, y, btn["text"], colors[btn["type"]])
                if not hovered:
                    hovering_button = None
                    hover_start_time = None
            else:
                hovering_button = None
                hover_start_time = None
                for btn in buttons:
                    x, y = btn["pos"]
                    draw_button(img, x, y, btn["text"], colors[btn["type"]])
    else:
        for btn in buttons:
            x, y = btn["pos"]
            draw_button(img, x, y, btn["text"], colors[btn["type"]])

    cv2.imshow("Gesture Calculator - OpenCV Only", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
