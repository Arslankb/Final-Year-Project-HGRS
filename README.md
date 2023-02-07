# Hand Gesture Recognition System

## Requirements:
- PyCharm 2021.22

### Requirements Python Modules:
- cv2
- mediapipe
- pyautogui
- win32api

### cv2
cv2 is the module import name for opencv-python.OpenCV is the huge open-source library for the computer vision, machine learning, and image processing and now it plays a major role in real-time operation which is very important in today's systems. By using it, one can process images and videos to identify objects, faces, or even handwriting of a human.

### mediapipe
MediaPipe is a framework for building cross-platform (i.e. Android, iOS, web, edge devices) multimodal (e.g. video, audio, any time series data) applied Machine Learning pipelines that consist of fast ML inference, classic computer vision, and media processing (e.g. video decoding). MediaPipe has released various prebuilt python and other language packages like:

- Object Detection
- Face Detection
- Hand Tracking
- Pose Estimation
- Multi-hand Tracking
- Hair Segmentation

### pyautogui
PyAutoGUI is essentially a Python package that works across Windows, MacOS X and Linux which provides the ability to simulate mouse cursor moves and clicks as well as keyboard button presses.

### win32api
You can use PyWin32 to locate or move the mouse cursor.
SetCursorPos() method moves the position of the mouse cursor to the position of the input tuple (x, y).

## Objectives:
- To build a system which recognizes the real time gesture display by user using Histogram-approach model. 
- Build a such system which can perform multiple functionality of systems by gesturing.
- without using keyboard and mouse and perform their functionality very well.
- Any File or Folder Functionality like (Copy, Paste, Cut, Del, Prop. and etc basically overall functionality)
- Any Document Reading
- Control multimedia (Video: play/pause, Video: forward/backword, Volume: Up/Down)
- Control Dino Game

# Programming for Media Controller, Game Controller & Folders/Files Functionality

Complete code for Controlling Media Player, Game Dino & File/Folder Functionality
basically we can handle mouse and keyboard functionality using Hand Gestures is given at the end of the document. Here we are explaining the important sections of the code for a better explanation.

Start the code by importing OpenCV, MediaPipe, and PyAutoGUI, win32api packages. As mentioned earlier MediaPipe is the core package for Hand Tracking while OpenCV is used for image processing. PyAutoGUI is used to control the keyboard according to gestures. win32api is used to locate or move the mouse curso.

    import cv2
    import mediapipe as mp
    import pyautogui
    import win32api

In the next lines, we have created two new variables. The first one is mp_drawing which will be used to get all the drawing utilities from the MediaPipe python package and the second one is mp_hands that is used to import the Hand Tracking model.

    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

After that define a function called findPosition(). As the name suggests it is used to find X, Y coordinates of the Index, Middle, Ring and Pinky finger. Coordinates of all fingertips will be stored inside a variable called lmList[].

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
    
Then start the video streaming from Raspberry Pi camera with a frame height and width of 720, 640.

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

Then in the next line set up a new instance for mediapipe feed to access the Hand Tracking model that we imported earlier. We have also passed two keyword arguments i.e. minimum detection confidence and minimum tracking confidence. Next, we will read the video frames and store them in the image variable.

    with mp_hands.Hands(
        min_detection_confidence=0.8,
        min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        success, image = cap.read()
        
The image that we got from the video feed is originally in BGR format. So, in this line, we will first flip the image horizontally for a later selfie-view display, and then convert the BGR image to RGB. The image writeable flag is set to false.

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    
After that, we are going to pass the image through the Hand Tracking model to make the detections and store the results in a variable called ‘results’.

    results = hands.process(image)
    
Once the detections are complete, we set the image writeable flag to true and convert the RGB image to BGR.

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

Now, as we got the detection results, we will call the mp_drawing variable to normalize the pixel coordinates and call mp_hands to track hand and store result on point variable and first we get the index_finger_tip at variable point for using the cursor movement. We can use win32api.SetCursorPos().
SetCursorPos() method moves the position of the mouse cursor to the position of the input tuple (x, y).

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
                            # cv2.circle(image, (indexfingertip_x, indexfingertip_y), 10, (255, 0, 255), cv2.FILLED)

                        except:
                            pass
    
Now, as we got the detection results, we will call the mp_drawing variable to draw these detections on the image and connect all the detections using the drawing utilities that we imported earlier.

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

After that, we will call the findPosition() function to get the ids and coordinates of all the detections. These values will be stored inside a variable called lmList.

    lmList = fingerPosition(image)
    
Now that we have coordinates for all of the hand landmarks, we will use them to detect different hand gestures and the first of them is detecting whether the fist is open or closed. For that, we will compare the coordinates of tips of fingers [8, 12, 16, 20] and middle points [6, 10, 14, 19] and if the fingertips are below the middle points, then the fist is closed and vice versa.

    for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                if lmList[tipIds[id]][2] > lmList[tipIds[id] - 2][2]:
                    fingers.append(0)

Then in the next lines get the total number of fingers counted and save it in a variable called totalFingers.

    totalFingers = fingers.count(1)
    
Now that we got the number of fingers, we will use them to play and pause the video, Click and Right Click functionality of Mouse.

    if totalFingers == 4:
        state = "play"
    
    if totalFingers == 0 and state == "play":
        state = "pause"
        pyautogui.press('space')
        print("space")

    if totalFingers == 2 and state == "play":
        state = "pause"
        pyautogui.click()
        print("Click")

    if totalFingers == 3 and state == "play":
        state = "pause"
        pyautogui.click(button='right')
        print("Right options")

Then the next gesture that we want to detect are left, right, up, and down movement. To detect the left and right movement, first, we will get the X-coordinate of the index fingertip and if the values are less than 300 then it is left swipe and if the values are greater than 400 then it is right swipe.

    if totalFingers == 1:
        if lmList[8][1] < 300:
            print("left")
            pyautogui.press('left')
        if lmList[8][1] > 400:
            print("Right")
            pyautogui.press('Right')
            
Similarly, to detect up and down gestures we will get the Y-coordinates of the countFingers == 0, and if the values are less than 210, then it is the Up slide, and if the values are greater than 230 then it is the low slide.

    if totalFingers == 0:
        if lmList[9][2] < 210:
            print("Up")
            pyautogui.press('Up')
        if lmList[9][2] > 230:
            print("Down")
            pyautogui.press('Down
            
if the `s` key was pressed, break from the loop

    if key == ord("s"):
        break
        
# **Code**

    import cv2
    import mediapipe as mp
    import pyautogui
    from math import sqrt
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

    For webcam input:
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
                            # cv2.circle(image, (indexfingertip_x, indexfingertip_y), 10, (255, 0, 255), cv2.FILLED)

                        except:
                            pass

        if len(lmList) != 0:
            fingers = []
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                if lmList[tipIds[id]][2] > lmList[tipIds[id] - 2][2]:
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

        cv2.imshow("Media Controller, Game Controller , Any File Functionality (Cut, Copy, Del etc.) & Mouse Trace", image)
        key = cv2.waitKey(1) & 0xFF
        # if the `s` key was pressed, break from the loop
        if key == ord("s"):
            break
    cv2.destroyAllWindows()