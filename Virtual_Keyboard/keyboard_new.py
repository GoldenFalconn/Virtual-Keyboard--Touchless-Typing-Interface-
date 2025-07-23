# import cv2
# import cvzone
# from cvzone.HandTrackingModule import HandDetector
# import numpy as np
# import time
#
# # Setup
# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)
# detector = HandDetector(detectionCon=0.8, maxHands=1)
#
# # Define keys
# keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
#         ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
#         ["Z", "X", "C", "V", "B", "N", "M", "<", "Space"]]
#
# finalText = ""
#
# # Draw keyboard buttons
# def drawAll(img, buttonList):
#     for button in buttonList:
#         x, y = button.pos
#         w, h = button.size
#         cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
#         cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
#         cv2.putText(img, button.text, (x + 20, y + 65),
#                     cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
#     return img
#
# # Button class
# class Button():
#     def __init__(self, pos, text, size=[85, 85]):
#         self.pos = pos
#         self.text = text
#         self.size = size
#
# # Create button list
# buttonList = []
# for i in range(len(keys)):
#     for j, key in enumerate(keys[i]):
#         x = 100 * j + 50
#         y = 100 * i + 50
#         buttonList.append(Button([x, y], key))
#
# # Main loop
# while True:
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     hands, img = detector.findHands(img)
#
#     img = drawAll(img, buttonList)
#
#     if hands:
#         lmList = hands[0]["lmList"]
#         indexFinger = lmList[8]  # Index finger tip
#         middleFinger = lmList[12]  # Middle finger tip
#
#         for button in buttonList:
#             x, y = button.pos
#             w, h = button.size
#
#             if x < indexFinger[0] < x + w and y < indexFinger[1] < y + h:
#                 cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
#                 cv2.putText(img, button.text, (x + 20, y + 65),
#                             cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
#
#                 # Check for click
#                 l, _, _ = detector.findDistance(lmList[8], lmList[12], img)
#                 if l < 40:
#                     if button.text == "Space":
#                         finalText += " "
#                     elif button.text == "<":
#                         finalText = finalText[:-1]
#                     else:
#                         finalText += button.text
#                     time.sleep(0.3)
#
#     # Show the typed text
#     cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
#     cv2.putText(img, finalText, (60, 430),
#                 cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
#
#     cv2.imshow("Virtual Keyboard", img)
#     key = cv2.waitKey(1)
#     if key == ord('q'):
#         break

#
# import cv2
# import mediapipe as mp
# import time
#
# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils
#
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
# cap = cv2.VideoCapture(0)
#
# keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
#         ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
#         ["Z", "X", "C", "V", "B", "N", "M", "<", "Space"]]
#
# finalText = ""
#
# class Button():
#     def __init__(self, pos, text, size=[85, 85]):
#         self.pos = pos
#         self.text = text
#         self.size = size
#
# buttonList = []
# for i in range(len(keys)):
#     for j, key in enumerate(keys[i]):
#         buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
#
# def drawAll(img, buttonList):
#     for button in buttonList:
#         x, y = button.pos
#         w, h = button.size
#         cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
#         cv2.putText(img, button.text, (x + 20, y + 65),
#                     cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
#     return img
#
# while True:
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(imgRGB)
#
#     drawAll(img, buttonList)
#
#     if results.multi_hand_landmarks:
#         for handLms in results.multi_hand_landmarks:
#             lmList = []
#             for id, lm in enumerate(handLms.landmark):
#                 h, w, _ = img.shape
#                 lmList.append([int(lm.x * w), int(lm.y * h)])
#
#             if lmList:
#                 x1, y1 = lmList[8]  # index tip
#                 x2, y2 = lmList[12] # middle tip
#
#                 for button in buttonList:
#                     x, y = button.pos
#                     w, h = button.size
#
#                     if x < x1 < x + w and y < y1 < y + h:
#                         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
#                         cv2.putText(img, button.text, (x + 20, y + 65),
#                                     cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
#
#                         # Check distance for click
#                         distance = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
#                         if distance < 40:
#                             if button.text == "Space":
#                                 finalText += " "
#                             elif button.text == "<":
#                                 finalText = finalText[:-1]
#                             else:
#                                 finalText += button.text
#                             time.sleep(0.3)
#
#             mp_drawing.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
#
#     # Display typed text
#     cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
#     cv2.putText(img, finalText, (60, 430),
#                 cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
#
#     cv2.imshow("Virtual Keyboard", img)
#     if cv2.waitKey(1) == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()













import cv2
import mediapipe as mp
import time

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Webcam input
cap = cv2.VideoCapture(0)

# Keyboard layout
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
    ["Space", "<", "Enter"]
]

finalText = ""
keyPressed = False
pressTime = 0

# Button class
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size

# Create all buttons
buttonList = []
for i in range(len(keys)):
    row = keys[i]
    for j, key in enumerate(row):
        x = 100 * j + 50
        y = 100 * i + 50
        if key == "Space":
            buttonList.append(Button([x, y], key, [500, 85]))
        else:
            buttonList.append(Button([x, y], key))

# Draw buttons with a blue-ish theme
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        # Pleasant blue-purple gradient color
        cv2.rectangle(img, (x, y), (x + w, y + h), (100, 100, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (240, 240, 255), 4)
    return img

# Fullscreen window setup
cv2.namedWindow("Virtual Keyboard", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Virtual Keyboard", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (1280, 720))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    drawAll(img, buttonList)
    currentTime = time.time()

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for lm in handLms.landmark:
                h, w, _ = img.shape
                lmList.append([int(lm.x * w), int(lm.y * h)])

            if lmList:
                x1, y1 = lmList[8]   # Index tip
                x2, y2 = lmList[12]  # Middle tip

                for button in buttonList:
                    x, y = button.pos
                    w, h = button.size

                    if x < x1 < x + w and y < y1 < y + h:
                        # Active hover color: light blue
                        cv2.rectangle(img, (x, y), (x + w, y + h), (80, 180, 255), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                        # Click detection
                        distance = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
                        if distance < 40 and not keyPressed:
                            keyPressed = True
                            pressTime = currentTime
                            if button.text == "Space":
                                finalText += " "
                            elif button.text == "<":
                                finalText = finalText[:-1]
                            elif button.text == "Enter":
                                finalText += "\n"
                            else:
                                finalText += button.text

            mp_drawing.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    # Debounce
    if keyPressed and time.time() - pressTime > 0.5:
        keyPressed = False

    # Display text box
    cv2.rectangle(img, (50, 600), (1200, 680), (130, 80, 200), cv2.FILLED)
    cv2.putText(img, finalText, (60, 660),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

    # Show the frame
    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
