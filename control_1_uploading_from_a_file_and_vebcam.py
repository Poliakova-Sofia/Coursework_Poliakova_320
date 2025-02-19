import cv2 # import the OpenCV library for working with videos

def play_video(source=0):
    cap = cv2.VideoCapture(source)  # open the video stream from the specified source (file or webcam)
    
    if not cap.isOpened(): # checking the opening of a video
        print("Error: Could not open video source")
        return
        # frames = []
    while True:
        ret, frame = cap.read()  # frame reading
        if not ret:
            print("Error: Failed to read frame or video ended")
            break
        # frames.append(frame)
        cv2.imshow("Original Video", frame)  # display the original video in the window.
        
        # converting a frame from BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        cv2.imshow("RGB Video", frame_rgb)  # display the converted RGB video.
        
        if cv2.waitKey(30) & 0xFF == ord('a'): # exit the loop and close the windows
            break  # by pressing 'a'
    
    cap.release() # release the video stream
    cv2.destroyAllWindows() # close all OpenCV windows

# launch from a file or webcam 
play_video("Avia.mp4")  # file name or 0 for webcam
