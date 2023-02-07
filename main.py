import cv2
import mediapipe as mp
import pyautogui
import win32api

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
##################################
tipIds = [4, 8, 12, 16, 20]
state = None
Gesture = None
wCam, hCam = 720, 640
pyautogui.FAILSAFE = False

############################
def fingerPosition(images, handNo=0):
    lmLists = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for ids, lm in enumerate(myHand.landmark):
            # print(id,lm)
            h, w, c = images.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmLists.append([id, cx, cy])
    return lmLists

# For webcam input:
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
with mp_hands.Hands(
        min_detection_confidence=0.8,
        min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        lmList = fingerPosition(image)
        # print(lmList)

        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                for point in mp_hands.HandLandmark:

                    normalizedLandmark = handLandmarks.landmark[point]
                    pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, wCam, hCam)

                    point = str(point)

                    if point == 'HandLandmark.INDEX_FINGER_TIP':
                        try:
                            indexfingertip_x = pixelCoordinatesLandmark[0]
                            indexfingertip_y = pixelCoordinatesLandmark[1]
                            win32api.SetCursorPos((indexfingertip_x * 3, indexfingertip_y * 3))

                        except:
                            pass

        if len(lmList) != 0:
            fingers = []
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    # state = "Play"
                    fingers.append(1)
                if (lmList[tipIds[id]][2] > lmList[tipIds[id] - 2][2]):
                    # state = "Pause"
                    # pyautogui.press('space')
                    # print("Space")
                    fingers.append(0)
            totalFingers = fingers.count(1)

            if totalFingers == 4:
                state = "play"

            if totalFingers == 2 and state == "play":
                state = "pause"
                pyautogui.click()
                print("Click")

            if totalFingers == 3 and state == "play":
                state = "pause"
                pyautogui.click(button='right')
                print("Right options")

            if totalFingers == 1:
                if lmList[8][1] < 300:
                    print("left")
                    pyautogui.press('left')
                if lmList[8][1] > 400:
                    print("Right")
                    pyautogui.press('Right')

            if totalFingers == 0:
                if lmList[9][2] < 210:
                    print("Up")
                    pyautogui.press('Up')
                if lmList[9][2] > 230:
                    print("Down")
                    pyautogui.press('Down')

            if totalFingers == 0 and state == "play":
                state = "pause"
                pyautogui.press('space')
                print("space")

        cv2.imshow("Media Controller & Mouse Trace", image)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    cv2.destroyAllWindows()