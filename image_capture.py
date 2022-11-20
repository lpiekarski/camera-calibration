import cv2
import os
from cam.camera import Camera

screenshot_idx = 0
cv2.namedWindow("Image Capture")
cam = Camera(quality=8)

while True:
    cam.keep_stream_alive()
    img = cam.get_frame()

    keypress = cv2.pollKey() & 0xFF
    if keypress == ord('q'):
        break
    elif keypress == ord(' '):
        filename = f'screenshots/screenshot{screenshot_idx:03d}.png'
        while os.path.exists(filename):
            screenshot_idx += 1
            filename = f'screenshots/screenshot{screenshot_idx:03d}.png'
        cv2.imwrite(filename, img)
        screenshot_idx += 1

    found, corners = cv2.findChessboardCorners(img, (5, 8))
    if found:
        cv2.drawChessboardCorners(img, (5, 8), corners, found)
    cv2.imshow("Image Capture", img)
