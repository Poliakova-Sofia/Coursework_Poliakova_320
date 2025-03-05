import cv2 # import library for working with videos
import numpy as np # import library for working with mathematical expressions and matrices

def load_video(source=0):  # open the video stream from the specified source (file or webcam)
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():  # checking the opening of a video
        print("Error: Could not open video source")
        return None
    return cap

def convert_to_rgb(frame): # converting a frame to RGB
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
def play_video(source=0):
    cap = load_video(source) # open the video stream from the specified source (file or webcam)
    if cap is None:
        return
    
    try:
        shear_factor = float(input("Enter the bevelling factor: "))
    except ValueError:
        print("Error: Invalid input. Please enter a numerical value.")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame or video ended")
            break
        
        # display the original video in the window
        cv2.imshow("Original Video", frame)
        
        # display the converted RGB video
        frame_rgb = convert_to_rgb(frame)
        cv2.imshow("RGB Video", frame_rgb)
        
        if cv2.waitKey(30) & 0xFF == ord('a'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


play_video("Avia.mp4")
