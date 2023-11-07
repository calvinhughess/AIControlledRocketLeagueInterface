# AI-Controlled Rocket League Interface

## Overview
This script automates car control in Rocket League by tracking the car's position through computer vision. It requires the car to be green for accurate tracking, as it uses a green gradient mask to differentiate the car from the background. The script provides automated keyboard inputs to steer the car towards the ball and allows manual inputs for different kickoff strategies.

## Features
- **Green Car Tracking**: Utilizes a green gradient to track the car's position.
- **Automated Steering**: Guides the car towards the ball without user input.
- **Kickoff Routine**: Supports manual keyboard inputs for six different kickoff positions.

## Requirements
- Python 3.x
- OpenCV (`cv2`) for image processing and computer vision.
- `pyautogui` for screen capture.
- `numpy` for array manipulations.
- `PIL` for additional image processing.
- `keyboard` for capturing keyboard events.
- `ctypes` for synthesizing keyboard events.
- `time` for managing event timing.

## Setup
1. Install Python 3.x on your system.
2. Install the necessary Python packages:
   ```shell
   pip install opencv-python pyautogui numpy pillow keyboard
   ```
3. Run the script with Rocket League open in borderless or windowed mode at a 1920x1080 resolution.

## Usage
- On script launch, it starts tracking the green car.
- For kickoffs, press the number keys (1-6) to execute the corresponding kickoff routine.

## Customization
- Modify `roi` vertices, color thresholds, and other parameters to fit your setup.
- Adjust the kickoff routine logic in the `kickoff_routine` function as needed.

## Additional Information
- The car in the game must be primarily green to be detected correctly by the script.
- Screen resolution is assumed to be 1920x1080 for the region of interest calculations.

## Disclaimer
This tool is for educational purposes and should not be used in violation of game policies. Using scripts for automation may contravene Rocket League's terms of service. Use responsibly and at your own risk.
