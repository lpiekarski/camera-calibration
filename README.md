# Camera Calibration
This repository contains a code that can be used to calibrate an ESP32 camera. The implementation of the `cam` package that is used here to get frames from the camera may or may not need to be modified to comply to the camera you are using.

## Installation
After cloning the repository simply run `pip install -r requirements.txt` and you're all set to go.

## Running demonstration
Run script `calibration.py` - it will take all the example images from `screenshots/` directory and perform a camera calibration based on them. After the calibration the program will draw a raw realtime stream of frames from the camera and below it a rectified version of the same stream after applying the calibration.

## Performing the Calibration
First off you need to print the [chessboard calibration pattern](calib_pattern.pdf). Then run the `image_capture.py` script and using spacebar capture around 20 images of the chessboard from different angles and using different parts of the camera screen. These images will be saved to `screenshots/` directory which already contains a few sample images of the chessboard, so if you want to run a calibration only based on your new images you have to delete them prior to this. Secondly run `calibration.py`. All the images used for the calibration will be displayed one by one with the chessboard pattern drawn on them. After this process you will get stream of frames from your calibrated camera side-by-side to the image from before the calibration for comparison.

## Example
Below are presented images used for calibration:

<img src="screenshots/screenshot000.png" alt="screenshot000" width="200"/>
<img src="screenshots/screenshot001.png" alt="screenshot001" width="200"/>
<img src="screenshots/screenshot002.png" alt="screenshot002" width="200"/>
<img src="screenshots/screenshot003.png" alt="screenshot003" width="200"/>
<img src="screenshots/screenshot004.png" alt="screenshot004" width="200"/>
<img src="screenshots/screenshot005.png" alt="screenshot005" width="200"/>
<img src="screenshots/screenshot006.png" alt="screenshot006" width="200"/>
<img src="screenshots/screenshot007.png" alt="screenshot007" width="200"/>
<img src="screenshots/screenshot008.png" alt="screenshot008" width="200"/>
<img src="screenshots/screenshot009.png" alt="screenshot009" width="200"/>
<img src="screenshots/screenshot010.png" alt="screenshot010" width="200"/>
<img src="screenshots/screenshot011.png" alt="screenshot011" width="200"/>
<img src="screenshots/screenshot012.png" alt="screenshot012" width="200"/>
<img src="screenshots/screenshot013.png" alt="screenshot013" width="200"/>
<img src="screenshots/screenshot014.png" alt="screenshot014" width="200"/>
<img src="screenshots/screenshot015.png" alt="screenshot015" width="200"/>
<img src="screenshots/screenshot016.png" alt="screenshot016" width="200"/>
<img src="screenshots/screenshot017.png" alt="screenshot017" width="200"/>
<img src="screenshots/screenshot018.png" alt="screenshot018" width="200"/>
<img src="screenshots/screenshot019.png" alt="screenshot019" width="200"/>

After running `calibration.py` on those images we get side-by-side view of images before and after calibration (difference is barely visible because the camera used here had already pretty good image prior to calibration):

<img src="examples/before_after_000.png" alt="before_after_000" width="200" style="margin: 50px"/>
<img src="examples/before_after_001.png" alt="before_after_001" width="200" style="margin: 50px"/>
<img src="examples/before_after_002.png" alt="before_after_002" width="200" style="margin: 50px"/>
<img src="examples/before_after_003.png" alt="before_after_003" width="200" style="margin: 50px"/>
<img src="examples/before_after_004.png" alt="before_after_004" width="200" style="margin: 50px"/>
<img src="examples/before_after_005.png" alt="before_after_005" width="200" style="margin: 50px"/>
<img src="examples/before_after_006.png" alt="before_after_006" width="200" style="margin: 50px"/>
<img src="examples/before_after_007.png" alt="before_after_007" width="200" style="margin: 50px"/>
<img src="examples/before_after_008.png" alt="before_after_008" width="200" style="margin: 50px"/>
<img src="examples/before_after_009.png" alt="before_after_009" width="200" style="margin: 50px"/>
