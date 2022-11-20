import cv2
import os
import numpy as np

from cam.camera import Camera

screenshot_dir = "screenshots/"

pattern_size = 30
ny = 5
nx = 8


def objpoints(pattern_size=30, nx=8, ny=5):
    res = np.zeros((nx * ny, 3), np.float32)
    res[:, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)
    return pattern_size * res


object_points = []
image_points = []
image_size = None
for image_filename in os.listdir(screenshot_dir):
    path = os.path.join(screenshot_dir, image_filename)
    print(f"Finding chessboard on image '{path}'")
    img = cv2.imread(path)
    found, corners = cv2.findChessboardCorners(img, (nx, ny))
    if found:
        print("\tChessboard found")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        size = (gray.shape[1], gray.shape[0])
        if image_size is None:
            image_size = size
        elif size != image_size:
            print(f"Image '{path}' has invalid size (Expected: {image_size}, got: {size})")
            continue
        term_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        corner_sub_pix = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), term_criteria)
        cv2.drawChessboardCorners(img, (nx, ny), corner_sub_pix, found)
        cv2.imshow("Calibration", img)
        cv2.waitKey()
        object_points.append(objpoints())
        image_points.append(corner_sub_pix)
    else:
        print("\tChessboard not found")

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, image_size, None, None)

print(mtx)
print(dist)

alpha = 1
rect_camera_matrix = cv2.getOptimalNewCameraMatrix(mtx, dist, image_size, alpha)[0]
map1, map2 = cv2.initUndistortRectifyMap(mtx, dist, np.eye(3), rect_camera_matrix, image_size, cv2.CV_32FC1)

cam = Camera(quality=8)
screenshot_idx = 0
while True:
    cam.keep_stream_alive()
    img = cam.get_frame()
    rect_img = cv2.remap(img, map1, map2, cv2.INTER_LINEAR)
    cv2.imshow("Calibration", cv2.vconcat([img, rect_img]))
    keypress = cv2.pollKey() & 0xFF
    if keypress == ord('q'):
        break
    elif keypress == ord(' '):
        filename = f'screenshots/before_after_{screenshot_idx:03d}.png'
        while os.path.exists(filename):
            screenshot_idx += 1
            filename = f'screenshots/before_after_{screenshot_idx:03d}.png'
        cv2.imwrite(filename, cv2.vconcat([img, rect_img]))
        screenshot_idx += 1
