# importing the required packages
import pyautogui
import cv2
import numpy as np
from PIL import Image
import time
from directkeys import PressKey, ReleaseKey, W, A, S, D, P, L, K
import keyboard


# Specify resolution
resolution = (1920, 1080)
 
# Specify video codec
codec = cv2.VideoWriter_fourcc(*"XVID")
 
# Specify name of Output file
filename = "Recording.avi"
 
# Specify frames rate. We can choose any
# value and experiment with it
fps = 60.0

prevCircle = None
 
dist = lambda x1, y1, x2, y2: (x1-x2)**2*(y1-y2)**2
 
green = [0, 255, 0]


prev_area = 0

kickoff_in_progress = False


# Creating a VideoWriter object
out = cv2.VideoWriter(filename, codec, fps, resolution)
 
# Create an Empty window
cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
 
# Resize this window
cv2.resizeWindow("Live", 1280, 720)

def get_car_mask(frame, lower_color, upper_color):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    return mask

def calculate_steering_angle(car_angle, desired_angle, angle_difference_threshold=5, smoothing_factor=0.5):
    angle_difference = desired_angle - car_angle

    if abs(angle_difference) < angle_difference_threshold:
        return 0

    adjusted_angle = angle_difference * smoothing_factor

    return int(adjusted_angle)

# Choose some points to track
def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

def kickoff_routine(position):
    global kickoff_in_progress
    kickoff_in_progress = True
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(P)
    ReleaseKey(L)

    if position == 1:
        #left corner
        PressKey(W)
        PressKey(L)
        time.sleep(1.7)
        PressKey(A)
        time.sleep(0.5)
        PressKey(P)
        time.sleep(0.1)
        ReleaseKey(P)
        PressKey(P)
        time.sleep(0.5)
        pass
    elif position == 2:
        #left middle
        PressKey(W)
        PressKey(L)
        time.sleep(2.3)
        PressKey(D)
        time.sleep(0.6)
        PressKey(P)
        time.sleep(0.1)
        ReleaseKey(P)
        PressKey(P)
        time.sleep(0.5)
        pass
    elif position == 3:
        #middle
        PressKey(W)
        PressKey(L)
        time.sleep(2.5)
        PressKey(P)
        time.sleep(0.1)
        ReleaseKey(P)
        PressKey(P)
        time.sleep(0.5)
        pass
    elif position == 4:
        #right middle
        PressKey(W)
        PressKey(L)
        time.sleep(2.3)
        PressKey(A)
        time.sleep(0.6)
        PressKey(P)
        time.sleep(0.1)
        ReleaseKey(P)
        PressKey(P)
        time.sleep(0.5)
        pass
    elif position == 5:
        #left corner
        PressKey(W)
        PressKey(L)
        time.sleep(1.7)
        PressKey(D)
        time.sleep(0.5)
        PressKey(P)
        time.sleep(0.1)
        ReleaseKey(P)
        PressKey(P)
        time.sleep(0.5)
        pass
        pass
    elif position == 6:
        # Execute kickoff routine for position 6
        pass
    else:
        print("Invalid kickoff position")
    
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(P)
    ReleaseKey(L)
    time.sleep(1)
    kickoff_in_progress = False

def on_key_press(event):
    global kickoff_in_progress
    if not kickoff_in_progress and event.name.isdigit() and 1 <= int(event.name) <= 6:
        kickoff_routine(int(event.name))

# Add this line to bind the callback function to key press events
keyboard.on_press(on_key_press)

while True:
   
   
    # Take screenshot using PyAutoGUI
    img = pyautogui.screenshot()
 
    # Convert the screenshot to a numpy array
    frame = np.array(img)
    
    # 1. Define the region of interest (ROI) - adjust the percentages as needed
    height, width = frame.shape[:2]
    roi_top = int(height * 0.6)
    roi_bottom = height
    roi_left = int(width * 0.25)
    roi_right = int(width * 0.75)

    # 2. Crop the image to keep only the ROI
    cropped_frame = frame[roi_top:roi_bottom, roi_left:roi_right]

    lower_color = np.array([40, 100, 100])
    upper_color = np.array([70, 255, 255])


    # Convert it from BGR(Blue, Green, Red) to
    # RGB(Red, Green, Blue)
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(grayFrame, (17,17), 0)
    vertices = np.array([[1620, 1480],[1620, 780],[2220, 780],[2220, 1480]], np.int32)
    blurFrame = roi(blurFrame, [vertices])
    
    circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1.1, 1000, 
                               param1=70, param2=50, minRadius=0, maxRadius=1000)
 
    if circles is not None:
        circles = np.uint16(np.around(circles))
        chosen = None
        for i in circles[0, :]:
            if chosen is None: chosen = i
            if prevCircle is not None:
                if dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) <= dist(i[0], i[1], prevCircle[0], prevCircle[1]):
                    chosen = i
        cv2.circle(frame, (chosen[0], chosen[1]), 1, (0, 100, 100), 3)
        cv2.circle(frame, (chosen[0], chosen[1]), chosen[2], (255, 0, 255), 3)
        prevCircle = chosen
    
    
   # Convert it from BGR(Blue, Green, Red) to
    # RGB(Red, Green, Blue)
    hsv_img = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([40, 70, 120])
    upper_color = np.array([90, 255, 255])
    mask = cv2.inRange(hsv_img, lower_color, upper_color)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    area_threshold = 20000
    # Draw a bounding box around the largest contour (assuming it's the car)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(max_contour)
        curr_area = w * h

        # Compare the areas to determine if the current area is bigger or smaller
        print("The area is " + str(curr_area))
        print("The width is " + str(w))
        print("The height is " + str(h))
       
        # Calculate the deviation from the center of the cropped frame
        center_x = x + w // 2
        deviation = center_x - cropped_frame.shape[1] // 2

        # Set a threshold for deviation to adjust the car's position
        deviation_threshold = 5
        if not kickoff_in_progress:
            if curr_area < area_threshold:

                #if the car is upsidedown, jump
                if curr_area < 5000:
                    ReleaseKey(W)
                    ReleaseKey(A)
                    ReleaseKey(D)
                    PressKey(P)
                    time.sleep(0.2)
                    ReleaseKey(P)
                    PressKey(P)
                    time.sleep(0.2)
                    ReleaseKey(P)
                    print("Car upsidedown")

                elif w > h:
                    #if angled diagonally sideways
                    if w > 330 :
                        if abs(deviation) > deviation_threshold :
                            if deviation > 0:
                                # Turn left
                                ReleaseKey(D)
                                PressKey(A)
                                PressKey(W)
                                PressKey(K)
                                time.sleep(0.1)
                                ReleaseKey(K)
                                ReleaseKey(A)
                                print("Diagonal turn left")
                            else :
                                ReleaseKey(A)
                                PressKey(D)
                                PressKey(W)
                                PressKey(K)
                                time.sleep(0.1)
                                ReleaseKey(K)
                                ReleaseKey(D)
                                print("Diagonal Turn Right")
                    #if straight, go straight
                    elif curr_area < 15000:
                        ReleaseKey(A)
                        ReleaseKey(D)
                        PressKey(W)
                        print("Going Straight")
                    #turn a little if not entirely straight
                    elif abs(deviation) > deviation_threshold :
                        if deviation > 0:
                            # Turn left
                            ReleaseKey(D)
                            PressKey(A)
                            PressKey(W)
                            PressKey(K)
                            time.sleep(0.1)
                            ReleaseKey(K)
                            ReleaseKey(A)
                            print("Close turn left")
                        else :
                            ReleaseKey(A)
                            PressKey(D)
                            PressKey(W)
                            PressKey(K)
                            time.sleep(0.1)
                            ReleaseKey(K)
                            ReleaseKey(D)
                            print("Close turn right")
                #if backwards, turn left
                elif h > w:
                    ReleaseKey(D)
                    PressKey(A)
                    PressKey(P)
                    time.sleep(0.5)
                    PressKey(W)
                    ReleaseKey(P)
                print("Curr Area used")
            else:
                if h > w :
                    PressKey(A)
                    PressKey(W)
                    print("Turn Around")

                elif -15 <= abs(deviation) <= 15:
                    ReleaseKey(A)
                    ReleaseKey(D)
                    PressKey(W)
                    print("Straight time")
                #turn if not straight
                elif abs(deviation) > deviation_threshold:
                    if deviation > 0:
                        # Turn left
                        ReleaseKey(D)
                        PressKey(A)
                        PressKey(W)
                        print(deviation)
                        print("The car is turning left.")
                    else:
                        # Turn right
                        ReleaseKey(A)
                        PressKey(D)
                        PressKey(W)
                        print(deviation)
                        print("The car is turning right.")
                    # You can add a small sleep here to give time for the car to adjust its position
                 
                else:
                    # Go straight
                    ReleaseKey(A)
                    ReleaseKey(D)
                    PressKey(W)
                    
                    
                    print("The car is going straight.")
            
        # Update the previous area with the current area for the next comparison
        
        cv2.rectangle(frame, (x + roi_left, y + roi_top), (x + w + roi_left, y + h + roi_top), (255, 0, 0), 3)

        prev_area = curr_area

    # Optional: Display the recording screen
   # cv2.imshow('Live', frame)
     
    # Stop recording when we press 'q'
    if cv2.waitKey(1) == ord('q'):
        break
 
# Release the Video writer
out.release()
 
# Destroy all windows
cv2.destroyAllWindows()
