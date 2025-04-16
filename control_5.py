import cv2 # import library for working with videos
import numpy as np # import library for working with mathematical expressions and matrices

def load_video(source=0):  # open the video stream from the specified source (file or webcam)
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():  # checking the opening of a video
        print("Error: Could not open video source")
        return None
    return cap
def risize_video(frame):
    original_height, original_width = frame.shape[:2]
    new_width = 600
    aspect_ratio = new_width / original_width
    new_height = int(original_height * aspect_ratio)
    return cv2.resize(frame, (new_width,new_height) )
def bilateral_filter(frame, diameter, sigma_color, sigma_space):
    # using Bilateral filter to a frame
    return cv2.bilateralFilter(frame, diameter, sigma_color, sigma_space)

def play_video(source=0):
    cap = load_video(source) # open the video stream from the specified source (file or webcam)
    if cap is None:
        return
    try:
        diameter = int(input("Enter filter diameter (from 5 to 25): "))
        sigma_color = int(input("Enter the sigmaColor value (from 50 to 200): "))
        sigma_space = int(input("Enter a sigmaSpace value (from 50 to 200): "))
    except ValueError:
        print("Input error! Default values are used.")
        diameter = 15
        sigma_color = 75
        sigma_space = 75

    while True:
        ret, source_frame = cap.read()
        frame = risize_video(source_frame)
        if not ret:
            print("Error: Failed to read frame or video ended")
            break
        
        # display the original video in the window
        cv2.imshow("Original Video", frame)

        # display the bilateral filter video
        bilateral = bilateral_filter(frame, diameter, sigma_color, sigma_space)
        cv2.imshow("Bilateral Filter Video", bilateral)

        if cv2.waitKey(30) & 0xFF == ord('a'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


play_video("Avia.mp4")
