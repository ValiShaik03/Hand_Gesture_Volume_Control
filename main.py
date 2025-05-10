# main.py

import cv2
import numpy as np
import time
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

################################
wCam, hCam = 640, 480
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

detector = htm.HandDetector(detectionCon=0.7, maxHands=1)

# pycaw setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]

# Smooth transition setup
smoothVol = 0
alpha = 0.2  # smoothing factor

volBar = 400
volPer = 0
volText = "MUTE"  # Default volume text
volColor = (0, 0, 255)  # Default volume color (Red)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Thumb tip and index finger tip
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 10, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 255, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 3)
        cv2.circle(img, (cx, cy), 8, (0, 0, 255), cv2.FILLED)

        length = np.hypot(x2 - x1, y2 - y1)

        # Convert Length to Volume Percentage
        volPer = np.interp(length, [20, 200], [0, 100])

        # Smooth transition for volume
        smoothVol = alpha * volPer + (1 - alpha) * smoothVol

        # Set system volume based on smoothed volume
        volume.SetMasterVolumeLevelScalar(smoothVol/100, None)

        # Mute if fingers very close
        if length < 20:
            volume.SetMasterVolumeLevelScalar(0.0, None)

        # Volume Level Text and Color
        if smoothVol == 0:
            volText = "MUTE"
            volColor = (0, 0, 255)    # Red
        elif smoothVol <= 30:
            volText = "LOW"
            volColor = (0, 255, 0)    # Green
        elif smoothVol <= 70:
            volText = "MEDIUM"
            volColor = (0, 255, 255)  # Yellow
        else:
            volText = "HIGH"
            volColor = (255, 0, 0)    # Blue

        # Fancy volume progress circle
        cv2.ellipse(img, (cx, cy), (50, 50), 0, 0, int(smoothVol*3.6), (0, 255, 0), 7)

    # Draw volume bar
    volBar = np.interp(smoothVol, [0, 100], [400, 150])
    cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), volColor, cv2.FILLED)
    cv2.putText(img, f'{int(smoothVol)} %', (40, 430), cv2.FONT_HERSHEY_COMPLEX,
                1, volColor, 2)

    # Draw Volume Text
    cv2.putText(img, f'Volume: {volText}', (350, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, volColor, 3)

    # FPS Counter
    cTime = time.time()
    fps = 1 / (cTime - pTime + 0.0001)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10, 40),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gesture Volume Control - Simple Text & Colors", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
