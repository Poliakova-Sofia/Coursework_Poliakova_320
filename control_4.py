import cv2 # import library for working with videos
import numpy as np # import library for working with mathematical expressions and matrices

def load_video(source=0):  # open the video stream from the specified source (file or webcam)
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():  # checking the opening of a video
        print("Error: Could not open video source")
        return None
    return cap
def canny_frame(frame):
    # converts images in gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # different Canny thresholds
    edges_low = cv2.Canny(gray, 50, 150)   # low threshold
    edges_mid = cv2.Canny(gray, 100, 200)  # middle threshold
    edges_high = cv2.Canny(gray, 150, 250) # high threshold

    # combining frames for easy viewing
    combined = cv2.hconcat([edges_low, edges_mid, edges_high])
    return combined
def play_video(source=0):
    cap = load_video(source) # open the video stream from the specified source (file or webcam)
    if cap is None:
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame or video ended")
            break
        
        # display the original video in the window
        cv2.imshow("Original Video", frame)
        # display the canny video
        combined = canny_frame(frame)
        cv2.imshow("Canny Video", combined)

        if cv2.waitKey(30) & 0xFF == ord('a'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


play_video("Avia.mp4")
